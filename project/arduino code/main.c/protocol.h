// protocol.h Copyright (C) 2019 Douglas Inglis
// Lazy method of sending control messages over I2C
// [packet ID (2 Bytes)] [Length in bytes (1 Byte)] [data] [EOT/Next Packet]

#ifndef PROTOCOL_H
#define PROTOCOL_H

#include "common.h"

#ifdef ARDUINO
#define I2C_ADDRESS 0x04
#define I2C_PIN 13

#define ENDIANNESS_FIX 0 // Hack to make the protocol work properly on Intel and AVR

#else

#define ENDIANNESS_FIX 1 // Hack to make the protocol work properly on Intel and AVR

#endif

#define EOT 0x04

#define error(x, args...) printf("Error in %s (%s:%d) \"" x "\"\n", __FUNCTION__, __FILE__, __LINE__, ##args)
#define debug(...) printf(__VA_ARGS__)

typedef int(*packet_handler)(char* data, uint8_t len);

struct packet_type {
  uint16_t packet_id;
  packet_handler handler;
  struct packet_type* next;
};

extern struct packet_type* begin;

typedef struct tcp_packet_header {
  uint16_t packet_id;
  uint8_t data_len;

} tcp_packet_header;

typedef struct tcp_packet_footer {
  uint8_t eot;

} tcp_packet_footer;

void initialise_protocol();

#endif
