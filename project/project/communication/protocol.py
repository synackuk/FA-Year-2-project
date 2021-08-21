# protocol.py Copyright (C) 2019 Douglas Inglis
# Simple method of sending commands across the network
# [2B packet ID] [len 2B] [data] [EOT]

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
		# Initialise the list of handlers
		self.handlers = {
			START_PACKET_ID: maneouver.start_maneuver,
			STOP_PACKET_ID: maneouver.stop_maneuver,
			LOAD_PACKET_ID: maneouver.load_maneuver,
		}

	def decode_packet(self, packet):
		packet_id, data_size = struct.unpack("HH", packet[:HEADER_LEN]) # Unpack the packets first four bytes into a two byte packet ID and two byte packet length
		if data_size == 0:
			if packet_id in self.handlers:
				return self.handlers[packet_id]() # Call the handler with no arguments as there is no data payload
			else:
				return None	
		
		data = packet[HEADER_LEN:HEADER_LEN + data_size] # Otherwise get the data payload from the packet
		if packet_id in self.handlers:
			return self.handlers[packet_id](data.decode()) # Call the handler with the data payload as an argument
		else:
			return None
	
	def encode_packet(self, packet_data):
		packet = bytes()
		data = bytes(packet_data[1]) # encode the packet data as a bytes argument
		data_size = len(data) # Get the length of the packet data
		packet += struct.pack("HH", packet_data[0], data_size) # Encode the packet ID and data length as sixteen bit integers in the packet
		packet += data # Add the data to the packet
		packet += struct.pack("B", EOT) # Add an End of Transmission to the packet
		if len(packet) > 65536:
			print("Packet too long")
			return None
		return packet

	def build_command_packet(self, command, data):
		if command not in commands:
			return None
		packet_data = [commands[command], data] # Get the packet ID based on command sent
		return self.encode_packet(packet_data)