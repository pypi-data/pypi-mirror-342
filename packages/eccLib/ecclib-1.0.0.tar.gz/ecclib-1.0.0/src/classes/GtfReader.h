/*!
 @file GtfReader.h
 @brief This file defines the GtfReader object interface
*/

#ifndef GTFREADER_H
#define GTFREADER_H

#include <Python.h>

#include "../hashmap_ext.h"

/*!
 @defgroup GtfReader_class GtfReader
 @brief A module providing a reader for GTF files
*/

/*!
 @defgroup GtfFile_class GtfFile
 @brief A module providing a file object for GTF files
*/

/*!
 @struct GtfReader
 @brief A reader that reads GTF files
 @ingroup GtfReader_class
 @see GtfFile
 @see GtfDict
 @see parseGTF
*/
typedef struct {
    PyObject_HEAD union {
        /*!
            @brief The FILE that is being read
            @details During iteration this object is used to access file
           contents via getline()
            @note This is used if buff is NULL
        */
        FILE *file;
        /*!
            @brief The file object that is being read
            @details This is used to access the file contents
            @note This is used if buff is not NULL
        */
        PyObject *fileObj;
    };
    /*!
     @brief The buffer for getline to write to
     @note if NULL, indicates fileObj should be used
    */
    char *buff;
    /*!
     @brief The size of the buffer
    */
    size_t buffSize;
    /*!
        @brief The hashmap key cache
        @details This hashmap is used to store the attribute keys that are found
       in the GTF file. This is used to optimize memory usage
    */
    hashmap_t attr_keys;
    /*!
     @brief The hashmap value cache
     @details This hashmap is used to store the values that are found
        in the GTF file. This is used to optimize memory usage
    */
    hashmap_t attr_vals;
} GtfReader;

/*!
 @struct GtfFile
 @brief A file that holds GTF data
 @ingroup GtfFile_class
 @see GtfReader
*/
typedef struct {
    PyObject_HEAD
        /*!
         @brief The name of the file
        */
        const char *filename;
    /*!
     @brief The FILE object
     @details This is used to access the file contents
     @warning may be NULL
    */
    FILE *file;
} GtfFile;

/*!
 @brief The Python type definition for the GtfFile object
 @ingroup GtfFile_class
*/
extern PyTypeObject GtfFileType;

/*!
 @brief The Python type definition for the GtfReader object
 @ingroup GtfReader_class
*/
extern PyTypeObject GtfReaderType;

#endif
