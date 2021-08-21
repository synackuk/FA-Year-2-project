# __init__.py (communication.py) Copyright (C) 2019 Douglas Inglis
# Hub and spoke system for connecting various robots together over the network.
# Uses a UDP broadcast to discover if there's a master robot then uses TCP to recieve commands from the master robot

import socket
import requests
import _thread 
from time import sleep
from communication.protocol import Protocol
import sys

# Set the client and server ports 

CLIENT_PORT = 37025
SERVER_PORT = 37020

class Communication:

	def __init__(self, maneouver):
		self.maneouver = maneouver
		self.protocol = Protocol(maneouver) # Initialise the protocol class

	
		# Build the client socket settings

		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
		self.client.setblocking(0)
		self.client.settimeout(1)
	
		# Build the server socket settings

		self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

		self.server.setblocking(1)
	
		# Initialise variables

		self.master_socket = None

		self.clients = []



	# https://stackoverflow.com/a/28950776
	def get_main_ip(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			s.connect(('1.1.1.1', 1))
			IP = s.getsockname()[0]
		except:
			IP = '127.0.0.1'
		finally:
			s.close()
		return IP

	def wait_for_new_robot(self):
		while True:
			try:
				data, addr = self.server.recvfrom(16) # Recieve from server socket
				if data == b"anyone_home?" and not addr[0] == self.get_main_ip(): # Check if broadcast is request from robot and that the robot is not the current robot
					new_addr = (addr[0], CLIENT_PORT) # Set new port for response
					new_port = CLIENT_PORT + len(self.clients) # Determine the new port for the device to listen on
					self.server.sendto("Yes.{}".format(new_port).encode(), new_addr) # Send the response message 
					sleep(1)
					temp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initialise a new socket
					temp_sock.connect((addr[0], new_port)) # Connect to the new slave robot
					self.clients.append(temp_sock) # Add new slave robot to the list of slave robots
			except Exception as e:
				print("Exception: {}".format(e))

	def build_master_thread(self):
		self.server.bind(("", SERVER_PORT)) # Bind to server port on 0.0.0.0
		try:
			_thread.start_new_thread(self.wait_for_new_robot, ()) # Initialise new thread
		except Exception as e:
			print("Failed to start wait_for_new_robot thread : {}".format(e))

	def is_master(self):
		self.client.bind(("", CLIENT_PORT))  # Bind to client port on 0.0.0.0
		self.client.sendto(b"anyone_home?", ('<broadcast>', SERVER_PORT)) # Broadcast to server port to check if other robots are on the netwoek
		try:
			data, addr = self.client.recvfrom(16)
			if data[:4] == b"Yes.": # If there are other robots on the network
				self.client.close()
				port = int(data[4:]) # Get the port to listen on
				self.master_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.master_socket.bind(("", port)) # Listen on new port address 0.0.0.0
				self.master_socket.listen(1)
				self.master_socket = self.master_socket.accept()[0]
				print("Bound to port {}".format(port))
				self.maneouver.should_track = False
				return False
		except Exception as e:
			print("Exception: {}".format(e))
		self.client.close()
		return True

	def slave_wait_for_command(self):
		try:
			data = self.master_socket.recv(65536) # Wait for request of length upto sixteen KB
			if data == "": # If no data is recieved the socket has been disconnected
				sys.exit(0)
			return self.protocol.decode_packet(data) # Decode packet recieved
		except Exception as e:
			print("Exception: {}".format(e))

	def master_send_command(self, command, data):
			packet = self.protocol.build_command_packet(command, data) # Encode the command as a packet to be sent to the client
			for client in self.clients: # For each client robot
				try:
					client.sendall(packet) # Send the packet
				except Exception as e:
					print("Exception: {}".format(e))
					self.clients.remove(client) # If the client socket has been disconnected remove it from the list