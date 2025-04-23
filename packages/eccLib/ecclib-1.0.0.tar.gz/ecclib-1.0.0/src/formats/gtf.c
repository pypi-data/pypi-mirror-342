/*!
 @file gtf.c
 @brief Implementations for the GTF module
*/

#include "gtf.h"

#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include <Python.h>

#include "../classes/GtfDict.h"
#include "../common.h"

// https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md

#define GTF_NONE_VAL '.'

bool validGTFLineToParse(const char *line, size_t len) {
    return line[0] != '#' && len >= CORE_FIELD_COUNT &&
           strnchr(line, '\t', len) != NULL;
}

/*!
 @brief Converts a hex character to half a byte
 @param c the character to convert
 @return the half a byte represented by the character
*/
static inline uint8_t hex_to_byte(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if ((c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F')) {
        return (c & 0x0F) + 9;
    }
    return 0;
}

#define MAX_2 0x10000

#define MAX_4 0x110000

#define ishex(c)                                                               \
    ((c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F'))

/*!
 @brief Converts a percent encoded string to a Python unicode string
 @param str the token to convert
 @param len the length of the token
 @return a Python unicode string or NULL on error
*/
static PyObject *PyUnicode_FromPercentEncoded(const char *str, size_t len) {
    /* yes this is my own implementation of url decoding COMBINED with utf8
     decoding */
    Py_UCS4 max = CHAR_MAX; // 127
    Py_ssize_t resolved_len =
        len; // we need to find out how long the resolved string will be
    bool has_percent = false;
    for (size_t i = 0; i < len; i++) {
        if (str[i] < 0) {                  // uh oh encoding shenanigans
            if ((str[i] & 0xE0) == 0xC0) { // 2-byte sequence
                if (i + 1 < len && (str[i + 1] & 0xC0) == 0x80) {
                    if (max < MAX_2) {
                        max = MAX_2;
                    }
                    resolved_len--;
                }
            } else if ((str[i] & 0xF8) == 0xF0) { // 4-byte sequence
                if (i + 3 < len && (str[i + 1] & 0xC0) == 0x80 &&
                    (str[i + 2] & 0xC0) == 0x80 &&
                    (str[i + 3] & 0xC0) == 0x80) {
                    if (max < MAX_4) {
                        max = MAX_4;
                    }
                    resolved_len -= 3;
                }
            } else if (max < UCHAR_MAX) {
                max = UCHAR_MAX;
            }
        } else if (str[i] == '%' && i + 2 < len && ishex(str[i + 1]) &&
                   ishex(str[i + 2])) {
            resolved_len -= 2;
            has_percent = true;
        }
    }
    if (!has_percent) { // there is nothing to resolve
        if (max == CHAR_MAX) {
            return PyUnicode_DecodeASCII(str, len, NULL);
        } else {
            return PyUnicode_DecodeUTF8(str, len, NULL);
        }
    }
    /* we create a new string with the right length and a certain character
     width based on max */
    PyObject *res = PyUnicode_New(resolved_len, max);
    if (res == NULL) {
        return NULL;
    }
    void *data = PyUnicode_DATA(res);
    int kind = PyUnicode_KIND(res);
    // now we have to populate it
    size_t j = 0;
    for (size_t i = 0; i < len; i++) {
        Py_UCS4 c;
        if (str[i] == '%' && i + 2 < len && ishex(str[i + 1]) &&
            ishex(str[i + 2])) {
            char ch = hex_to_byte(str[i + 1]) << 4 | hex_to_byte(str[i + 2]);
            if (ch < 0) {
                PyErr_SetString(PyExc_ValueError,
                                "Failed while resolving percent encoding");
                Py_DECREF(res);
                return NULL;
            }
            c = (Py_UCS4)ch;
            i += 2;
        } else {
            if (max == MAX_4 && str[i] < 0) {
                c = (str[i] & 0x07) << 18 | (str[i + 1] & 0x3F) << 12 |
                    (str[i + 2] & 0x3F) << 6 | (str[i + 3] & 0x3F);
                i += 3;
            } else if (max == MAX_2 && str[i] < 0) {
                c = (str[i] & 0x1F) << 6 | (str[i + 1] & 0x3F);
                i++;
            } else {
                c = (Py_UCS4)str[i];
            }
        }
        PyUnicode_WRITE(kind, data, j, c);
        j++;
    }
    return res;
}

/*!
 @brief Looks up a string in the hashmap, and if it doesn't exist, creates it
 @param map the hashmap to look up the string in
 @param key the key to look up
 @param len the length of the key
 @return the found or created object as a new reference, or NULL on error
*/
static inline PyObject *lookup_str(hashmap_t *map, const char *key,
                                   size_t len) {
    // fprintf(stderr, "key: %.*s\n", len, key);
    PyObject *possible = hashmap_get(map, key, len);
    if (possible == NULL) {
        // fprintf(stderr, "put: %.*s\n", len, key);
        possible = PyUnicode_FromPercentEncoded(key, len);
        if (possible == NULL) {
            return NULL;
        }
        // MAYBE here avoid the conversion to utf8, the problem is, that key
        // must remain valid until the hashmap is destroyed
        Py_ssize_t key_len;
        const char *key_data = PyUnicode_AsUTF8AndSize(possible, &key_len);
        if (key_data == NULL) {
            Py_DECREF(possible);
            return NULL;
        }
        // one reference is consumed by the hashmap
        if (hashmap_put(map, key_data, key_len, possible) < 0) {
            Py_DECREF(possible);
            return NULL;
        }
    }
    // this reference is stored in the hashmap
    Py_INCREF(possible);
    return possible;
}

/*!
 @brief Adds a key-value pair to the GTF dictionary
 @param attributes the dictionary to add the key-value pair to
 @param attr_keys the cache of previously seen attribute keys
 @param attr_vals the cache of previously seen attribute values
 @param key the key to add
 @param keyLen the length of the key
 @param value the value to add
 @param valLen the length of the value
 @return -1 on error
 @details This is a convenience function to improve readability of the
    handleGTFAttributes function
*/
static inline int add_key_value(hashmap_t *restrict attributes,
                                hashmap_t *restrict attr_keys,
                                hashmap_t *restrict attr_vals,
                                const char *restrict key, size_t keyLen,
                                const char *restrict value, size_t valLen) {
    PyObject *restrict key_str = lookup_str(attr_keys, key, keyLen);
    if (key_str == NULL) {
        return -1;
    }
    PyObject *restrict pyValue = lookup_str(attr_vals, value, valLen);
    if (pyValue == NULL) {
        Py_DECREF(key_str);
        return -1;
    }
    Py_ssize_t key_str_len;
    const char *restrict key_str_data =
        PyUnicode_AsUTF8AndSize(key_str, &key_str_len);
    if (key_str_data == NULL) {
        Py_DECREF(key_str);
        Py_DECREF(pyValue);
        return -1;
    }
    /* We don't reuse the hash from earlier because the hashes
        are dependent on the hashmap size, which may differ */
    if (hashmap_put_tuple(attributes, key_str_data, key_str_len, key_str,
                          pyValue) < 0) {
        Py_DECREF(key_str);
        Py_DECREF(pyValue);
        return -1;
    }
    return 0;
}

/*!
 @brief Handles the attributes of a GTF line and adds them to the provided dict
 @param dict the dict to which the attributes should be added
 @param lastoccurrence the last occurrence of the attributes in the GTF line
 @param attr_keys set of previously seen attribute keys
 @param attr_vals set of previously seen attribute values
 @return -1 on error
 @details This function parses the key-value section of the GTF line. It
 utilizes a hashmap cache to store the keys of the attributes, and utilizes a
 unique encoding processing function
*/
static inline int handleGTFAttributes(GtfDict *dict,
                                      const occurrence_t *lastoccurrence,
                                      hashmap_t *restrict attr_keys,
                                      hashmap_t *restrict attr_vals) {
    Py_ssize_t attrLen = lastoccurrence->len;
    occurrence_t attroccurrence;
    int attrTokenRes =
        strtok_ri(lastoccurrence->token, ';', &attrLen, &attroccurrence);
    while (attrTokenRes > 0) {
        size_t offset = 0;
        while (attroccurrence.token[offset] == ' ') { // skip the spaces
            offset++;
        }
        while (attroccurrence.token[attroccurrence.len - 1] ==
               ' ') { // remove trailing spaces
            attroccurrence.len--;
        }
        if (offset < attroccurrence.len) { // if the token isn't empty by the
                                           // time we skipped all the spaces
            attroccurrence.token += offset;
            attroccurrence.len -= offset;
            for (uint32_t middleOffset = 0; middleOffset < attroccurrence.len;
                 middleOffset++) {
                if (attroccurrence.token[middleOffset] == ' ' ||
                    attroccurrence.token[middleOffset] == '=') {
                    const char *restrict value = attroccurrence.token +
                                                 middleOffset +
                                                 1; // and value the rest
                    size_t valLen = attroccurrence.len - middleOffset - 1;
                    // we need to remove potential quotation marks
                    if (*value == '"') {
                        value++;
                        valLen--;
                        if (value[valLen - 1] == '"') {
                            valLen--;
                        }
                    }
                    if (add_key_value(&dict->attributes, attr_keys, attr_vals,
                                      attroccurrence.token, middleOffset, value,
                                      valLen) < 0) {
                        return -1;
                    }
                    break;
                }
            }
        }
        attrTokenRes = strtok_ri(NULL, ';', &attrLen, &attroccurrence);
    }
    return 0;
}

/*!
 @brief Processes a token as a string
 @param token the token to process
 @param attr_vals the cache of previously seen attribute values
 @return the processed token
 @details This function processes a token as a string, meant to be used during
 core field parsing
*/
static inline PyObject *process_token_str(const occurrence_t *token,
                                          hashmap_t *attr_vals) {
    if (token->token[0] == GTF_NONE_VAL) {
        Py_INCREF(Py_None);
        return Py_None;
    } else {
        return lookup_str(attr_vals, token->token, token->len);
    }
}

/*!
 @brief Processes a token as an integer
 @param token the token to process
 @return the processed token
*/
static inline PyObject *process_token_int(const occurrence_t *token) {
    if (token->token[0] == GTF_NONE_VAL) {
        Py_INCREF(Py_None);
        return Py_None;
    } else {
        const long val = strtol(token->token, NULL, 10);
        return PyLong_FromLong(val);
    }
}

GtfDict *createGTFdict(const occurrence_t *token, hashmap_t *restrict attr_keys,
                       hashmap_t *restrict attr_vals) {
    GtfDict *dict = PyObject_New(GtfDict, &GtfDictType);
    if (dict == NULL) {
        PyErr_SetString(PyExc_Exception, "Dict creation failed");
        return NULL;
    }
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &dict->attributes) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        return NULL;
    }
    bool valid = true;
    uint8_t partsLen = 0;
    Py_ssize_t len = token->len;
    occurrence_t lastoccurrence = {NULL, 0};
    int tokenRes = strtok_ri(token->token, '\t', &len, &lastoccurrence);
    while (tokenRes > 0 && valid) {
        switch (partsLen) {
        case SEQNAME: {
            dict->seqname = process_token_str(&lastoccurrence, attr_vals);
            break;
        }
        case SOURCE: {
            dict->source = process_token_str(&lastoccurrence, attr_vals);
            break;
        }
        case FEATURE: {
            dict->feature = process_token_str(&lastoccurrence, attr_vals);
            break;
        }
        case START: {
            dict->start = process_token_int(&lastoccurrence);
            break;
        }
        case END: {
            dict->end = process_token_int(&lastoccurrence);
            break;
        }
        case SCORE: {
            if (lastoccurrence.token[0] != GTF_NONE_VAL) {
                PyObject *restrict score =
                    PyFloat_FromDouble(strtod(lastoccurrence.token, NULL));
                if (score == NULL) {
                    valid = false;
                    break;
                }
                dict->score = score;
            } else {
                dict->score = Py_None;
                Py_INCREF(Py_None);
            }
            break;
        }
        case REVERSE: {
            if (lastoccurrence.token[0] != GTF_NONE_VAL &&
                lastoccurrence.token[0] != '?') {
                if (lastoccurrence.token[0] == '-') {
                    dict->reverse = Py_True;
                } else {
                    dict->reverse = Py_False;
                }
            } else {
                dict->reverse = Py_None;
            }
            Py_INCREF(dict->reverse);
            break;
        }
        case FRAME: {
            dict->frame = process_token_int(&lastoccurrence);
            break;
        }
        case ATTRIBUTES: {
            // According to profiler 56% of parsing time is spent here
            valid = handleGTFAttributes(dict, &lastoccurrence, attr_keys,
                                        attr_vals) == 0;
            break;
        }
        }
        tokenRes = strtok_ri(NULL, '\t', &len, &lastoccurrence);
        partsLen++;
    }
    if (partsLen < CORE_FIELD_COUNT) {
        /* PyObject_New allocated necessary memory for the attributes, but it
         used malloc, potentially leaving garbage in the memory this can throw
         off PyXDECREF NULL checks, so we need to set the attributes to NULL
         that are not set I actually haven't seen this happen in runtime, but
         it did manage to crash Valgrind */
        for (; partsLen < CORE_FIELD_COUNT; partsLen++) {
            dict->core[partsLen] = NULL;
        }
        Py_DECREF(dict);
        PyErr_SetString(PyExc_ValueError,
                        "Invalid column count in provided GTF line");
        return NULL;
    }
    if (!valid) { // error case
        Py_DECREF(dict);
        return NULL;
    }
    return dict;
}

char *gtf_percent_encode(const char *restrict str, size_t len,
                         size_t *restrict outLen) {
    char *res = malloc((len * 3) + 1);
    if (res == NULL) {
        return NULL;
    }
    size_t offset = 0;
    for (size_t i = 0; i < len; i++) {
        if (str[i] < ' ' || str[i] == 0x7F || (str[i] > '!' && str[i] < '-') ||
            str[i] == ';' || str[i] == '=') {
            percent_encode_char(res + offset, str[i]);
            offset += 3;
        } else {
            res[offset] = str[i];
            offset++;
        }
    }
    *outLen = offset;
    res[offset] = '\0';
    return res;
}

const char *keywords[] = {"seqname", "source", "feature", "start",
                          "end",     "score",  "reverse", "frame"};

const uint8_t keyword_sizes[CORE_FIELD_COUNT] = {7, 6, 7, 5, 3, 5, 7, 5};
