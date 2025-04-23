/*!
 @file functions.c
 @brief Functions for parsing files. Core of the library
*/

#include "functions.h"

#include <stdbool.h>
#include <stdlib.h>

#include <Python.h>

#include "classes/FastaBuff.h"
#include "classes/GeneList.h"
#include "classes/GtfDict.h"
#include "common.h"
#include "formats/fasta.h"
#include "formats/gtf.h"

#if __unix__
#include <sys/stat.h>
#include <unistd.h>
#endif

/*!
 @brief Struct for storing input data for parsing functions
*/
typedef struct {
    /*!
     @brief The string to parse
     @warning This should not be modified
    */
    const char *str;
    /*!
     @brief The length of the string
    */
    Py_ssize_t len;
    /*!
     @brief The PyUnicode object that holds the string
     @warning MAY BE NULL
    */
    PyObject *parent;
} input_t;

/*!
 @brief Checks if the input_t object is NULL
 @param input the input_t object to check
 @return true or false depending on if the input_t object is NULL
*/
#define input_t_is_NULL(input) (input.str == NULL)

/*!
 @brief NULL input_t object
 @return an input_t object with all fields set to NULL
*/
#define NULL_input_t                                                           \
    (input_t) { NULL, 0, NULL }

/*!
 @brief Frees the input_t object
 @param input the input_t object to free
*/
static void free_input_t(input_t input) {
    if (input.parent != NULL) {
        Py_DECREF(input.parent);
    } else {
        free((void *)input.str);
    }
}

/*!
 @brief Gets file contents object for parsing from python function arguments
 @details For performance reasons this function will attempt to get the file
 size using seek() and tell() if the object has those methods and then load the
 entire file using read(). If the object doesn't have seek() then it will just
 call read(-1).
 @param first the first argument
 @return a input_t object containing the file contents
 @note first needs to be either a string or have a read method
*/
static input_t getFileContentsFromArgs(PyObject *restrict first) {
    input_t result;
    if (PyUnicode_Check(first)) {
        Py_INCREF(first);
        result.parent = first;
    } else {
#ifdef __unix__
        { // exclusive to systems that have read() and fstat() so POSIX afaik
            int fd = PyObject_AsFileDescriptor(first);
            if (fd >= 0) {
                // If the object can be converted to a file descriptor
                struct stat sb;
                if (fstat(fd, &sb) != 0) {
                    PyErr_SetFromErrno(PyExc_OSError);
                    return NULL_input_t;
                }
                result.len = sb.st_size;
                char *restrict buff = malloc(result.len);
                if (buff == NULL) {
                    return NULL_input_t;
                }
                ssize_t read_num = 0;
                while (read_num < (ssize_t)result.len) {
                    ssize_t read_result =
                        read(fd, buff + read_num, result.len - read_num);
                    if (read_result < 0) {
                        PyErr_SetFromErrno(PyExc_OSError);
                        free(buff);
                        return NULL_input_t;
                    } else if (read_result == 0) {
                        break;
                    }
                    read_num += read_result;
                }
                result.str = buff;
                result.parent = NULL;
                return result;
            } else {
                PyErr_Clear();
            }
        }
#endif
        if (PyObject_HasAttrString(first, "seek") == false) {
            result.parent = PyObject_CallMethod(first, "read", "i", -1);
        } else {
            PyObject *seek = PyObject_CallMethod(first, "seek", "ii", 0, 2);
            if (seek == NULL) {
                return NULL_input_t;
            }
            Py_DECREF(seek);
            PyObject *size = PyObject_CallMethod(first, "tell", NULL);
            if (size == NULL) {
                return NULL_input_t;
            }
            seek = PyObject_CallMethod(first, "seek", "ii", 0, 0);
            if (seek == NULL) {
                Py_DECREF(size);
                return NULL_input_t;
            }
            Py_DECREF(seek);
            result.parent = PyObject_CallMethod(first, "read", "O", size);
            Py_DECREF(size);
        }
        if (result.parent == NULL) {
            return NULL_input_t;
        }
        if (!PyUnicode_Check(result.parent)) {
            PyErr_SetString(PyExc_Exception, "File contents must be a string");
            Py_DECREF(result.parent);
            return NULL_input_t;
        }
    }
    result.str = PyUnicode_AsUTF8AndSize(result.parent, &result.len);
    return result;
}

/*!
 @brief Adds an entry to the FASTA tuple
 @param list the list to add the entry to
 @param title the title of the entry
 @param titleLen the length of the title
 @param seq the sequence of the entry
 @return the result of PyList_Append
 @see FastaBuff
*/
static inline int addFasta(PyObject *list, const char *restrict title,
                           size_t titleLen, PyObject *seq) {
    PyObject *key = PyUnicode_DecodeUTF8(title, titleLen, NULL);
    if (key == NULL) {
        return -1;
    }
    PyObject *value;
    int res;
    if (seq != NULL) {
        value = seq;
    } else {
        value = Py_None;
        Py_INCREF(value);
    }
    PyObject *entry = PyTuple_Pack(2, key, value);
    Py_DECREF(value);
    Py_DECREF(key);
    if (entry == NULL) {
        return -1;
    }
    res = PyList_Append(list, entry);
    Py_DECREF(entry);
    return res;
}

/*!
 @brief Echoes progress to a file
 @details Echoes the progress of lineIndex/total to the file
 @param echo the file to echo to
 @param lineIndex the current line index
 @param total the total amount of lines
*/
static inline void echoProgress(PyObject *restrict echo, unsigned int lineIndex,
                                unsigned int total) {
    float progress;
    if (total == 0) { // well we can't divide by zero so this
        progress = 100.0;
    } else {
        progress = ((float)lineIndex / (float)total) * 100;
    }
    char echoStr[100]; // i really doubt we can exceed this limit, even so it
                       // won't crash just not print out the entire number, yes
                       // i know I can use math.h to figure out the needed size
    snprintf(echoStr, sizeof(echoStr), "%d/%d(%.2f%%)\r", lineIndex, total,
             progress);
    PyFile_WriteString(echoStr, echo);
}

/*!
 @brief Processes a chunk of FASTA text data
 @param chunk the chunk of data to process
 @param chunk_size the size of the chunk
 @param result the list to append the FASTA entries to
 @param title the title of the current entry
 @param titleLen the length of the title
 @return true if an error occurred, false otherwise
*/
static bool processTextData(const char *restrict chunk, Py_ssize_t chunk_size,
                            PyObject *restrict result,
                            const char *restrict title, Py_ssize_t titleLen) {

    PyObject *seq = PyUnicode_New(chunk_size, 127);
    if (seq == NULL) {
        return true;
    }
    void *restrict data = PyUnicode_DATA(seq);
    size_t j = 0;
    for (size_t i = 0; i < (size_t)chunk_size; i++) {
        if (!IS_LETTER_CHAR(chunk[i])) {
            continue;
        }
        PyUnicode_WRITE(PyUnicode_1BYTE_KIND, data, j, chunk[i]);
        j++;
    }
    // standard break, probably bad
    ((PyASCIIObject *)seq)->length = j;
    if (addFasta(result, title, titleLen, seq) < 0) {
        Py_DECREF(seq);
        return true;
    }
    return false;
}

/*!
 @brief Processes a chunk of binary FASTA data
 @param chunk the chunk of data to process
 @param chunk_size the size of the chunk
 @param result the list to append the FASTA entries to
 @param title the title of the current entry
 @param titleLen the length of the title
 @return true if an error occurred, false otherwise
*/
static bool processBinaryData(const char *restrict chunk, Py_ssize_t chunk_size,
                              PyObject *restrict result,
                              const char *restrict title, Py_ssize_t titleLen) {
    // the number of allocated bytes for sequence
    size_t sequenceBufferSize = (size_t)ceilf(chunk_size / 2.0f);
    // here we overallocate, but it's better than reallocating
    uint8_t *sequenceBuffer = malloc(sequenceBufferSize);
    if (sequenceBuffer == NULL) {
        PyErr_SetFromErrno(PyExc_MemoryError);
        return true;
    }
    uint8_t el[2];    // buffer for storing the last two elements
    bool RNA = false; // if we have a U in the sequence
    bool elIndex = 0; // index of the last element in el
    // number of CHARACTERS, so usually 2x the number of bytes
    size_t seq_i = 0;
    size_t buff_i = 0;
    for (size_t i = 0; i < (size_t)chunk_size; i++) {
        // skip newlines
        if (!IS_LETTER_CHAR(chunk[i])) {
            continue;
        }
        if (chunk[i] == 'U') {
            RNA = true;
        }
        el[elIndex] = fasta_binary_mapping[chunk[i]];
        if (el[elIndex] == i_Index) {
            char err[] = "Invalid character '\0'";
            err[19] = chunk[i];
            PyErr_SetString(PyExc_ValueError, err);
            free(sequenceBuffer);
            return true;
        }
        if (elIndex) {
            sequenceBuffer[buff_i] = toByte(el[0], el[1]);
            buff_i++;
        }
        seq_i++;
        elIndex = !elIndex;
    }
    if (seq_i == 0) {
        free(sequenceBuffer);
        if (addFasta(result, title, titleLen, NULL) < 0) {
            return true;
        }
    } else {
        if (elIndex) { // if we have an odd number of characters
            sequenceBuffer[buff_i] = toByte(el[0], 0);
            buff_i++;
        }
        if (buff_i != sequenceBufferSize) {
            sequenceBufferSize = buff_i;
            // realloc the buffer
            uint8_t *reallocd = realloc(sequenceBuffer, sequenceBufferSize);
            if (reallocd == NULL) {
                PyErr_SetFromErrno(PyExc_MemoryError);
                free(sequenceBuffer);
                return true;
            } else {
                sequenceBuffer = reallocd;
            }
        }
        FastaBuff *seq =
            FastaBuff_new(sequenceBuffer, sequenceBufferSize, seq_i, RNA);
        if (addFasta(result, title, titleLen, (PyObject *)seq) < 0) {
            free(sequenceBuffer);
            return true;
        }
    }
    return false;
}

PyObject *parseFasta(PyObject *self, PyObject *args,
                     PyObject *restrict kwargs) {
    UNUSED(self);
    static const char *keywords[] = {"file", "binary", "echo", NULL};
    PyObject *restrict first;
    PyObject *restrict binary = Py_True;
    PyObject *restrict echo = Py_None;
    if (PyArg_ParseTupleAndKeywords(args, kwargs, "O|OO", (char **)keywords,
                                    &first, &binary, &echo) != true) {
        return NULL;
    }
    input_t input = getFileContentsFromArgs(first);
    if (input_t_is_NULL(input)) {
        return NULL;
    }
    uint32_t seq_count = 0; // technically we don't need to have anything
                            // assigned to this, but it's good to have it
    if (!Py_IsNone(echo)) {
        seq_count = strncount(input.str, '>', input.len);
    }
    PyObject *result = PyList_New(0);
    if (result == NULL) {
        free_input_t(input);
        return NULL;
    }
    uint32_t seq_index = 1;

    const char *str = input.str;
    while (*str != '>') {
        str++;
        input.len--;
    }
    str++;
    input.len--;

    bool (*processor)(const char *restrict, Py_ssize_t, PyObject *restrict,
                      const char *restrict, Py_ssize_t) =
        Py_IsTrue(binary) ? processBinaryData : processTextData;

    occurrence_t lastoccurrence;
    int tokResult = strtok_ri(str, '>', &input.len, &lastoccurrence);
    while (tokResult > 0) {
        if (!Py_IsNone(echo)) {
            echoProgress(echo, seq_index, seq_count);
        }
        const char *title_end =
            strnchr(lastoccurrence.token, '\n', lastoccurrence.len);
        if (title_end == NULL || title_end == lastoccurrence.token) {
            // insert a None sequence if there is no sequence
            if (addFasta(result, lastoccurrence.token, lastoccurrence.len,
                         NULL) < 0) {
                free_input_t(input);
                Py_DECREF(result);
                return NULL;
            }
        } else {
            size_t titleLen = title_end - lastoccurrence.token;
            // number of characters in chunk
            size_t chunk_size = lastoccurrence.len - titleLen - 1;
            const char *restrict chunk = title_end + 1;
            if (processor(chunk, chunk_size, result, lastoccurrence.token,
                          titleLen)) {
                free_input_t(input);
                Py_DECREF(result);
                return NULL;
            }
        }
        tokResult = strtok_ri(NULL, '>', &input.len, &lastoccurrence);
        if (PyErr_CheckSignals() < 0) {
            free_input_t(input);
            Py_DECREF(result);
            return NULL;
        }
        seq_count++;
    }
    free_input_t(input);
    if (!Py_IsNone(echo)) {
        PyFile_WriteString("\n", echo);
    }
    return result;
}

PyObject *parseGTF(PyObject *restrict self, PyObject *restrict args,
                   PyObject *restrict kwargs) {
    UNUSED(self);
    static const char *keywords[] = {"file", "echo", NULL};
    PyObject *restrict first;
    PyObject *restrict echo = Py_None;
    if (PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", (char **)keywords,
                                    &first, &echo) != true) {
        return NULL;
    }
    input_t input = getFileContentsFromArgs(first);
    if (input_t_is_NULL(input)) {
        return NULL;
    }
    unsigned int lineCount = 0;
    if (!Py_IsNone(echo)) {
        lineCount = strncount(input.str, '\n', input.len);
    }
    // NOTE from my testing it seems that finding the accurate size is not worth
    // it. Seems like Python Lists are built for appending and it doesn't care
    // if no size is given Now naturally it would be nice to give it a size,
    // appending is still worse than simply writing, but the cost of processing
    // the entire file to get an accurate final size is simply too high
    PyObject *restrict result = GeneList_new(0);
    if (result == NULL) {
        free_input_t(input);
        return NULL;
    }
    hashmap_t attr_keys, attr_vals;
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &attr_keys) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        free_input_t(input);
        Py_DECREF(result);
        return NULL;
    }
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &attr_vals) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        free_input_t(input);
        Py_DECREF(result);
        hashmap_destroy_py(&attr_keys);
        return NULL;
    }
    unsigned int lineIndex = 1;
    occurrence_t lastoccurrence;
    int tokRes = strtok_ri(input.str, '\n', &input.len, &lastoccurrence);
    while (tokRes > 0) {
        if (!Py_IsNone(echo)) {
            echoProgress(echo, lineIndex, lineCount);
        }
        if (validGTFLineToParse(lastoccurrence.token, lastoccurrence.len)) {
            GtfDict *dict =
                createGTFdict(&lastoccurrence, &attr_keys, &attr_vals);
            if (dict != NULL) {
                int res = PyList_Append(result, (PyObject *)dict);
                Py_DECREF(dict);
                if (res != 0) {
                    free_input_t(input);
                    Py_DECREF(result);
                    hashmap_destroy_py(&attr_keys);
                    hashmap_destroy_py(&attr_vals);
                    return NULL;
                }
            } else {
                free_input_t(input);
                Py_DECREF(result);
                hashmap_destroy_py(&attr_keys);
                hashmap_destroy_py(&attr_vals);
                return NULL;
            }
        } else if (strncmp(lastoccurrence.token, "##FASTA", 7) ==
                   0) { // GFFv3 files CAN have FASTA sequences at the end, so
                        // we need to check for that
            break;
        }
        tokRes = strtok_ri(NULL, '\n', &input.len, &lastoccurrence);
        if (PyErr_CheckSignals() < 0) {
            free_input_t(input);
            Py_DECREF(result);
            hashmap_destroy_py(&attr_keys);
            hashmap_destroy_py(&attr_vals);
            return NULL;
        }
        lineIndex++;
    }
    free_input_t(input);
    if (!Py_IsNone(echo)) {
        PyFile_WriteString("\n", echo);
    }
    hashmap_destroy_py(&attr_keys);
    hashmap_destroy_py(&attr_vals);
    return result;
}
