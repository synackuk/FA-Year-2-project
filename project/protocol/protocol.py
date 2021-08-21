# protocol.py Copyright (C) 2019 Douglas Inglis
# Lazy method of sending control messages 
# [2B packet ID] [Byte len 2B] [data] [EOT]

import struct
import binascii

HEADER_LEN = 4
EOT = 0x04

START_PACKET_ID = 0x5354
STOP_PACKET_ID = 0x5350
LOAD_PACKET_ID = 0x4C44

commands = {
	"start" : START_PACKET_ID,
	"stop"	: STOP_PACKET_ID,
	"load"  : LOAD_PACKET_ID,
}

class Protocol:

	def __init__(self, maneouver):
		self.handlers = {
			START_PACKET_ID: maneouver.start_maneuver,
			STOP_PACKET_ID: maneouver.stop_maneuver,
			LOAD_PACKET_ID: maneouver.load_maneuver,
		}

	def decode_packet(self, packet):
		packet_id, data_size = struct.unpack("HH", packet[:HEADER_LEN])
		if data_size == 0:
			if packet_id in HANDLERS:
				return self.handlers[packet_id]()
			else:
				return None	
		else:
			data = packet[HEADER_LEN:HEADER_LEN + data_size]
			if packet_id in HANDLERS:
				return self.handlers[packet_id](data)
			else:
				return None
	
	def encode_packet(self, packet_data):
		packet = bytes()
		data = bytes(packet_data[1])
		data_size = len(data)
		packet += struct.pack("HH", packet_data[0], data_size)
		packet += data
		packet += struct.pack("B", EOT)
		if len(packet) > 65536:
			print("Packet too long")
			return None
		return packet

	def build_command_packet(self, command, data):
		if command not in commands:
			return None
		packet_data = [commands[command], data]
		return self.encode_packet(packet_data)