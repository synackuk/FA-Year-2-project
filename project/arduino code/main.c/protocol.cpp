// protocol.c Copyright (C) 2019 Douglas Inglis
// Lazy method of sending control messages over I2C
// [packet ID (2 Bytes)] [Length in bytes (1 Byte)] [data] [EOT/Next Packet]

#include "protocol.h"

struct packet_type* begin;

int decode_packet(void* packet) {
  int ret;
  tcp_packet_header* header = packet;
  uint16_t packet_id = header->packet_id;
  uint8_t data_len = header->data_len;
  void* data = packet + sizeof(tcp_packet_header) - ENDIANNESS_FIX;
  tcp_packet_footer* footer = data + data_len;

  debug("packet id: 0x%x\n", packet_id);
  struct packet_type* current = begin;
  while(current != NULL) {
    if(current->packet_id == packet_id) {
      ret = current->handler(data, data_len);
      if(ret != 0) {
        error("Failed to execute packet handler");
        return -1;
      }
      break;
    }
    current = current->next;
  }
  if (footer->eot != EOT) {
    debug("footer->eot = 0x%x\n", footer->eot);
    ret = decode_packet(&footer->eot);
    if(ret != 0) {
      error("Failed to decode second packet");
      return -1;
    }
  }
  return 0;
}

int move_handler(char* data, uint8_t len) {
  if(len != 2) {
    error("Wrong packet length (%d)", len);
    return -1;
  }
  char direction = data[0];
  uint8_t distance = data[1];
  debug("Moving %c for %u\n", direction, distance);
  return 0;
}

int rotate_handler(char* data, uint8_t len) {
  if(len != 1) {
    error("Wrong packet length (%d)", len);
    return -1;
  }
  char direction = data[0];
  debug("Rotating %c\n", direction);
  return 0;
}

void initialise_protocol_packets() {
  begin = malloc(sizeof(struct packet_type));
  begin->packet_id = 0x4D56;
  begin->handler = &move_handler;
  struct packet_type* next = malloc(sizeof(struct packet_type));
  begin->next = next;
  next->packet_id = 0x524F;
  next->handler = &rotate_handler;
  next->next = NULL;
}
#ifdef ARDUINO

static void data_recieved(int count) {
  int ret = 0;
  int i = 0;
  uint8_t byte_recieved = 0;
  uint8_t packet[255];


  Wire.readBytes(packet, count);
  ret = decode_packet((void*) packet);
  if(ret != 0) {
    error("Failed to decode packet.");
    return;
  }
  return;

}

void initialise_i2c() {
  
  Wire.onReceive(data_recieved);
}

#endif

void initialise_protocol() {
  initialise_protocol_packets();
//#ifdef ARDUINO
  initialise_i2c();
//#endif
}
#ifndef ARDUINO

int main(){ // Simple test program if being executed on non-arduino hardware.
  initialise_protocol();
  decode_packet("VM\2F\x05\x04");
}
#endif
