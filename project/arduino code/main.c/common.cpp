// common.c Copyright (C) 2019 Douglas Inglis
// Common functions used throughout the codebase

#include "common.h"

int _printf(char* fmt, ...) {
  char buffer[256];
  va_list args;
  va_start (args, fmt);
  vsnprintf (buffer, 255, fmt, args);
  va_end (args);
  Serial.print (buffer);
  return 0;
}
