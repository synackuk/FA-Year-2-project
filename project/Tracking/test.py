from __future__ import print_function
import cv2
from ar_markers import detect_markers

class Tracking:

	def __init__(self):
		self.capture = cv2.VideoCapture(0)
		self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.view_centre = self.width / 2

	def get_frame(self):
		if self.capture.isOpened():
			frame_captured, frame = self.capture.read()
			if frame_captured:
				return frame

	def find_markers(self):
		frame = self.get_frame()
		markers = detect_markers(frame)
		for marker in markers:
			marker.highlite_marker(frame)
		cv2.imshow("Markers", frame)
		cv2.waitKey(1)
		if len(markers) == 0:
			return None
		return markers

	def find_direction_to_centre_marker(self, marker, tolerence = 50):
		if abs(marker.center[0] - self.view_centre) <= tolerence:
			return "stop"

		if marker.center[0] > self.view_centre:
			return "left"
		else:
			return "right"		

	def centre_car(self, tolerence = 50):
		while True:
			markers = self.find_markers()
			if not markers:
				continue
			for marker in markers:
				direction = self.find_direction_to_centre_marker(marker, tolerence)
				if direction == "stop":
					print("Current location of marker: {}".format(marker.center[0]))
					print("True centre: {}".format(self.view_centre))
					return True
				print("move the car {}.".format(direction))

if __name__ == '__main__':		
	track = Tracking()
	track.centre_car()