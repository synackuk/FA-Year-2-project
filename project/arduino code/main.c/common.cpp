#include "common.h"

int _printf(char* fmt, ...) {
  char buffer[256];
  va_list args;
  va_start (args, fmt);
  vsprintf (buffer,fmt, args);
  va_end (args);
  Serial.print (buffer);
  return 0;
}
