/*!
 @file GeneList.h
 @brief Contains the definition of the GeneList object
*/

#ifndef GENELIST_H
#define GENELIST_H

#include <Python.h>

/*!
 @defgroup GeneList_class GeneList
 @brief All methods and objects related to the GeneList object
 @details The GeneList object is a list that holds geneDicts. It is used to
 store the parsed GTF data. It exists to provide type checking and to allow for
 easy processing method implementation
*/

/*!
 @struct GeneList
 @brief A list that holds geneDicts
 @details The GeneList object is a list that holds geneDicts. It is used to
 store the parsed GTF data. It exists to provide type checking and to allow for
 easy processing method implementation
 @note This object is a subclass of the Python list object
 @see GtfDict
 @ingroup GeneList_class
*/
typedef struct {
    /*!
     @var list
     @brief The underlying list object
    */
    PyListObject list;
} GeneList;

/*!
 @brief The Python type definition for the GeneList object
 @ingroup GeneList_class
*/
extern PyTypeObject GeneListType;

/*!
 @brief Creates a new GeneList object
 @param len the length of the list
 @return a new GeneList object
*/
PyObject *GeneList_new(Py_ssize_t len);

/*!
 @brief Checks if the object is an instance of the GeneList type
 @param op the object to check
 @return 1 if the object is an instance of the GeneList type, 0 otherwise
*/
#define GeneList_Check(op) PyObject_TypeCheck(op, &GeneListType)

#endif
