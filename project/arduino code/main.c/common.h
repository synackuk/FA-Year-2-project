#ifndef COMMON_H
#define COMMON_H

#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <stdarg.h>
#include <Arduino.h> 
#include <Wire.h>

int _printf(char* fmt, ...);

#undef printf

#define printf _printf

#endif
