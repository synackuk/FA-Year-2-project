// main.c Copyright (C) 2019 Douglas Inglis
// Initialises the areas of this program 

#include "common.h"
#include "protocol.h"

void setup() {
  Wire.begin(I2C_ADDRESS);
  Serial.begin(9600);
  initialise_protocol();

}

void loop() {
  // put your main code here, to run repeatedly:

}
