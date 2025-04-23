/*!
 @file common.c
 @brief Contains implementations for common functions and structs used by the
 other modules
*/

#include "common.h"

#include <stdbool.h>
#include <stdlib.h>

#include <Python.h>

const char *strnchr(const char *restrict str, char c, size_t len) {
    for (size_t i = 0; i < len; i++) {
        if (str[i] == c) {
            return str + i;
        }
    }
    return NULL;
}

int strtok_ri(const char *restrict str, char delim, Py_ssize_t *restrict strLen,
              occurrence_t *restrict lastoccurrence) {
    if (*strLen == 0) {
        return 0;
    }
    if (str == NULL) {
        str = lastoccurrence->token + lastoccurrence->len + 1;
    }
    lastoccurrence->len = 0;
    for (; lastoccurrence->len < (size_t)*strLen; lastoccurrence->len++) {
        if (str[lastoccurrence->len] == delim) {
            (*strLen)--;
            break;
        }
    }
    lastoccurrence->token = str;
    *strLen -= lastoccurrence->len;
    return 1;
}

void percent_encode_char(char *restrict out, char c) {
    out[0] = '%';
    out[1] = "0123456789ABCDEF"[c >> 4];
    out[2] = "0123456789ABCDEF"[c & 0x0F];
}

uint32_t strncount(const char *restrict str, char c, size_t len) {
    uint32_t count = 0;
    for (size_t i = 0; i < len; i++) {
        if (str[i] == c) {
            count++;
        }
    }
    return count;
}

PyObject *ioMod = NULL;
