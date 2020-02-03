# protocol.py Copyright (C) 2019 Douglas Inglis
# Lazy method of sending control messages over I2C
# [2B packet ID] [Byte len 1B] [data] [EOT/Next Packet]

import struct
import binascii
#import smbus

HEADER_LEN = 3
EOT = 0x04

I2C_ADDRESS = 0x04

MOVE_PACKET_ID = 0x4D56
ROTATE_PACKET_ID = 0x524F

# Currently only needs to work RPI -> Arduino

#def handler1(data):
#	print(data)
#
#def handler2(data):
#	print(codecs.encode(data, 'hex'))
#
#HANDLERS = {
#	0x4142: handler1,
#	0x4344: handler2
#}
#
#def decode_packet(packet):
#	packet_id, data_size = struct.unpack("HB", packet[:HEADER_LEN])
#	data = packet[HEADER_LEN:HEADER_LEN + data_size]
#	eot = struct.unpack("B", packet[(HEADER_LEN + data_size):(HEADER_LEN + data_size + 5)])
#	if packet_id in HANDLERS:
#		HANDLERS[packet_id](data)
#	else:
#		pass
#	if eot != EOT:
#		decode_packet(packet[(HEADER_LEN + data_size + 4):])
#		pass

def encode_packet(packet_data):
	packet = bytes()
	for i in range(0 , len(packet_data)):
		data = bytes(packet_data[i][1])
		data_size = len(data)
		packet += struct.pack("HB", packet_data[i][0], data_size)
		packet += data
	packet += struct.pack("B", EOT)
	if len(packet) > 254:
		print("Packet too long")
		return None
	return packet

def send_packet(packet):
	print("sending packet \"{}\"".format(packet))
	#for i in len(packet):
	#	bus.write_byte(I2C_ADDRESS, packet[i])



def move(direction, distance):
	direction_byte = bytes(direction, "utf-8")[0]
	packet_data = [[MOVE_PACKET_ID, struct.pack("<BB", direction_byte, distance)]]
	movement_packet = encode_packet(packet_data)
	if movement_packet == None:
		print("Packet empty")
		return -1
	send_packet(movement_packet)
	return 0

def rotate(direction):
	direction_byte = bytes(direction, "utf-8")[0]
	packet_data = [[ROTATE_PACKET_ID, struct.pack("<B", direction_byte)]]
	rotate_packet = encode_packet(packet_data)
	if rotate_packet == None:
		print("Packet empty")
		return -1
	send_packet(rotate_packet)
	return 0

move("F", 5)
rotate("L")