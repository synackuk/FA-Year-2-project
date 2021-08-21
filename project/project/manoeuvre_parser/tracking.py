# tracking.py Copyright (C) 2019 Douglas Inglis
# Allows the robots to track eachother through the use of AI markers

from __future__ import print_function
import cv2
from ar_markers import detect_markers

class Tracking:

	def __init__(self):
		self.capture = cv2.VideoCapture(0) # Setup the video capture from a webcam
		self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH) # Get the width of the capture frame
		self.view_centre = self.width / 2 # Get the centre of the frame

	def get_frame(self):
		if self.capture.isOpened(): # Check if the capture is open
			frame_captured, frame = self.capture.read() # Read a single frame from the capture
			if frame_captured:
				return frame

	def find_markers(self):
		frame = self.get_frame()
		markers = detect_markers(frame) # Detect AI Markers in the frame
		for marker in markers:
			marker.highlite_marker(frame) # Highlight any markers found
		#cv2.imshow("Markers", frame)
		cv2.waitKey(1) # Allows the frame to update
		if len(markers) == 0:
			return None
		return markers

	def find_direction_to_centre_marker(self, marker, tolerence = 50):
		if abs(marker.center[0] - self.view_centre) <= tolerence: # If the absolute (magnitude) of the centre of the marker on the webcam frame is within the tolerence
			return "stop"

		if marker.center[0] > self.view_centre:
			return "left"
		else:
			return "right"

	def find_car(self, movement_funcs):
		markers = None
		i = 0
		while not markers and i != 25: # Until markers appear or there have been 25 steps
			movement_funcs.left(0.1) # Turn the car left
			markers = self.find_markers() # Try and find markers
			i += 1
		if not markers:
			return False
		return True

	def centre_car(self, movement_funcs, tolerence = 50):
		ret = 0
		while True:
			markers = self.find_markers() # Try and find markers
			if not markers:
				ret = self.find_car(movement_funcs) # Find the car 
				if ret == False:
					return False
				continue
			for marker in markers:
				direction = self.find_direction_to_centre_marker(marker, tolerence) # Get the nessecery direction to find the centre
				if direction == "stop":
					print("Current location of marker: {}".format(marker.center[0]))
					print("True centre: {}".format(self.view_centre))
					return True
				print("moving the car {}.".format(direction))
				if direction == "left":
					movement_funcs.left(0.1) # Move the car left to centre it in the webcam frame
				else:
					movement_funcs.right(0.1) # Move the car right to centre it in the webcam frame

if __name__ == '__main__':		
	track = Tracking()
	track.centre_car()