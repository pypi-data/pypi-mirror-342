/*!
 @file fasta.h
 @brief Header file for the FASTA module
 @details This module provides common functions that we use for handling FASTA
 data
*/

#ifndef FASTA_H
#define FASTA_H

#include <limits.h>
#include <stdbool.h>
#include <stdint.h>

/*!
 @defgroup fasta Fasta
 @brief Module providing functions for handling FASTA data
*/

/*!
 @def firstEl(b)
 @brief Gets the first 4 bits of a byte
 @param b the byte to get the first 4 bits from
 @ingroup fasta
*/
#define firstEl(b) (b & 0x0F) // first 4 bits
/*!
 @def secondEl(b)
 @brief Gets the second 4 bits of a byte
 @param b the byte to get the second 4 bits from
 @ingroup fasta
*/
#define secondEl(b) (b & 0xF0) >> 4 // second 4 bits
/*!
 @def toByte(a, b)
 @brief Combines two 4 bit numbers into a byte
 @param a the first 4 bit number
 @param b the second 4 bit number
 @ingroup fasta
*/
#define toByte(a, b) (uint8_t)a | (b << 4)
/*!
 @def i_Index
 @brief Invalid FASTA index
 @ingroup fasta
*/
#define i_Index 0xFF // invalid FASTA index

/*!
 @brief A lookup table mapping FASTA characters to binary values
 @warning This table is initialized in the initialize_fasta_binary_mapping
 @ingroup fasta
*/
extern uint8_t fasta_binary_mapping[CHAR_MAX + 1];

/*!
 @brief Returns IUPAC FASTA character
 @param index the code to convert to a character
 @param RNA if true, T will be converted to U
 @ingroup fasta
 @return the IUPAC character
 @warning index must be less than 16, else the function will go out of bounds
*/
char getIUPACchar(uint8_t index, bool RNA);

/*!
 @brief Initializes the FASTA binary mapping
 @ingroup fasta
*/
void initialize_fasta_binary_mapping();

#endif
