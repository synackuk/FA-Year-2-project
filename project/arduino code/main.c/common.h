// common.h Copyright (C) 2019 Douglas Inglis
// Common functions used throughout the codebase

#ifndef COMMON_H
#define COMMON_H

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdarg.h>
#include <Arduino.h> 
#include <Wire.h>

int _printf(char* fmt, ...); // Hack to enable us to print format strings over serial

#undef printf

#define printf _printf

#endif
