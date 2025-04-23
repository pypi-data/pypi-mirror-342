/*!
 @file GtfReader.c
 @brief Contains the implementation of the iterative GTF reader
*/

#include "GtfReader.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <Python.h>

#include "../formats/gtf.h"
#include "GtfDict.h"

// GTF file class definition

#define BUFFSIZE 1024

/*!
 @brief Saves the provided filename and checks if it exists
 @param self
 @param args standard python argument tuple
 @param kwds unsupported!
 @return -1 on error
 @ingroup GtfFile_class
*/
static int GtfFile_init(GtfFile *self, PyObject *args, PyObject *kwds) {
    UNUSED(kwds);
    if (!PyArg_ParseTuple(args, "s", &self->filename)) {
        return -1;
    }
    self->file = NULL;
    return 0;
}

/*!
 @brief Opens the file for reading
 @param self
 @param args standard python argument tuple
 @return self or NULL on error
 @ingroup GtfFile_class
*/
static PyObject *GtfFile_enter(GtfFile *self, PyObject *args) {
    UNUSED(args);
    if (self->file != NULL) {
        PyErr_SetString(PyExc_IOError, "GTF file is already open");
        return NULL;
    }
    self->file = fopen(self->filename, "r");
    Py_INCREF(self);
    return (PyObject *)self;
}

/*!
 @brief Closes the file
 @param self
 @param args standard python argument tuple
 @param kwds unsupported!
 @return None or NULL on error
 @ingroup GtfFile_class
*/
static PyObject *GtfFile_exit(GtfFile *self, PyObject *args, PyObject *kwds) {
    UNUSED(args);
    UNUSED(kwds);
    if (self->file == NULL) {
        PyErr_SetString(PyExc_IOError, "GTF file is not open");
        return NULL;
    }
    fclose(self->file);
    Py_INCREF(Py_None);
    return Py_None;
}

/*!
 @brief Creates a GtfReader object from the GtfFile
 @param self
 @return a GtfReader object or NULL on error
 @ingroup GtfFile_class
*/
static PyObject *GtfFile_iter(GtfFile *self) {
    if (self->file == NULL) {
        PyErr_SetString(PyExc_IOError, "GTF file is not open");
        return NULL;
    }
    fseek(self->file, 0, SEEK_SET); // reset the file
    GtfReader *reader = PyObject_New(GtfReader, &GtfReaderType);
    if (reader == NULL) {
        return NULL;
    }
    // initialize the reader
    reader->file = self->file;
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &reader->attr_keys) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        return NULL;
    }
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &reader->attr_vals) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        hashmap_destroy_py(&reader->attr_keys);
        return NULL;
    }
    reader->buff = malloc(BUFFSIZE);
    if (reader->buff == NULL) {
        hashmap_destroy_py(&reader->attr_keys);
        hashmap_destroy_py(&reader->attr_vals);
        PyErr_SetString(PyExc_MemoryError, "Failed to allocate buffer");
        return NULL;
    }
    reader->buffSize = BUFFSIZE;
    return (PyObject *)reader;
}

/*!
 @brief Methods for the GtfFile class
*/
static PyMethodDef GtfFile_methods[] = {
    {"__enter__", (PyCFunction)GtfFile_enter, METH_NOARGS, ""},
    {"__exit__", (PyCFunction)GtfFile_exit, METH_VARARGS, ""},
    {NULL, NULL, 0, NULL} /* Sentinel */
};

PyTypeObject GtfFileType = {PyVarObject_HEAD_INIT(NULL, 0).tp_name =
                                "eccLib.GtfFile",
                            .tp_basicsize = sizeof(GtfFile),
                            .tp_doc = PyDoc_STR("Just a GtfReader factory"),
                            .tp_itemsize = 0,
                            .tp_flags = Py_TPFLAGS_DEFAULT,
                            .tp_new = PyType_GenericNew,
                            .tp_init = (initproc)GtfFile_init,
                            .tp_iter = (getiterfunc)GtfFile_iter,
                            .tp_methods = GtfFile_methods};

// GTF reader class definition

/*!
 @brief Initializes the GtfReader
 @param self
 @param args standard python argument tuple
 @param kwds unsupported!
*/
static int GtfReader_init(GtfReader *self, PyObject *args, PyObject *kwds) {
    UNUSED(kwds);
    PyObject *first = PyTuple_GET_ITEM(args, 0);
    if (first == NULL) {
        return -1;
    }
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &self->attr_keys) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        return -1;
    }
    if (hashmap_create_xh(DEFAULT_ATTR_SIZE, &self->attr_vals) < 0) {
        PyErr_SetString(PyExc_Exception, "Failed to create hashmap");
        hashmap_destroy_py(&self->attr_keys);
        return -1;
    }
    Py_INCREF(first);
    self->fileObj = first;
    self->buff = NULL;
    return 0;
}

/*!
 @brief Retrieves the next line of the opened file and tries parsing it
 @param self
 @return NULL on error or GtfDict
 @ingroup GtfReader_class
*/
static PyObject *GtfReader_next(GtfReader *restrict self) {
    if (self->file == NULL) {
        PyErr_SetString(PyExc_IOError, "GTF file has been closed");
        return NULL;
    }
    occurrence_t line;
    if (self->buff != NULL) {
        do {
            char *result = fgets(self->buff, self->buffSize, self->file);
            if (result != NULL) {
                line.token = self->buff;
                line.len = strlen(self->buff);
            } else {
                if (feof(self->file)) {
                    PyErr_SetNone(PyExc_StopIteration);
                    return NULL;
                } else {
                    PyErr_SetString(PyExc_IOError, "Failed to read line");
                    return NULL;
                }
            }
        } while (!validGTFLineToParse(line.token, line.len));
        return (PyObject *)createGTFdict(&line, &self->attr_keys,
                                         &self->attr_vals);
    } else {
        PyObject *lineObj = NULL;
        do {
            Py_XDECREF(lineObj);
            lineObj = PyFile_GetLine(self->fileObj, -1);
            if (lineObj == NULL) {
                if (PyErr_ExceptionMatches(PyExc_EOFError)) {
                    PyErr_SetNone(PyExc_StopIteration);
                }
                return NULL;
            }
            line.token =
                PyUnicode_AsUTF8AndSize(lineObj, (Py_ssize_t *)&line.len);
            if (line.token == NULL) {
                return NULL;
            }
        } while (!validGTFLineToParse(line.token, line.len));
        PyObject *res = (PyObject *)createGTFdict(&line, &self->attr_keys,
                                                  &self->attr_vals);
        Py_DECREF(lineObj);
        return res;
    }
}

/*!
 @brief Deallocates the GtfReader
 @param self
 @ingroup GtfReader_class
*/
static void GtfReader_dealloc(GtfReader *restrict self) {
    if (self->buff != NULL) {
        free(self->buff);
    } else {
        Py_DECREF(self->fileObj);
    }
    hashmap_destroy_py(&self->attr_keys);
    hashmap_destroy_py(&self->attr_vals);
    PyObject_Free(self);
}

PyTypeObject GtfReaderType = {
    PyVarObject_HEAD_INIT(NULL, 0).tp_name = "eccLib.GtfReader",
    .tp_basicsize = sizeof(GtfReader),
    .tp_doc = PyDoc_STR("A iterable reader of GTF dicts from a GTF file"),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc)GtfReader_init,
    .tp_iternext = (iternextfunc)GtfReader_next,
    .tp_dealloc = (destructor)GtfReader_dealloc};
