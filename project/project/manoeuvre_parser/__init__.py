import _thread
from manoeuvre_parser.movement import Movement
from manoeuvre_parser.tracking import Tracking

class Maneuver:

	def command_start(self, args):
		print("started maneuver")	

	def command_stop(self, args):
		if not self.continuous or self.stop:
			print("stopping maneuver")
			self.running = False
			exit(0)

	def command_move(self, args):
		direction = args.pop(0).strip()
		distance = int(args.pop(0).strip())
		print("Moving {} {} steps".format(direction, distance))	
		if direction == "forward":
			self.movement.forward(distance)
		elif direction == "backward":
			self.movement.backward(distance)
		elif direction == "left":
			self.movement.left(distance)
		elif direction == "right":
			self.movement.right(distance)

	def command_centre(self, args):
		if not self.should_track:
			return
		self.tracking.centre_car(self.movement)

	def command_move_relative(self, args):
		ret = 0
		if not self.should_track:
			return
		direction = args.pop(0).strip()
		distance = int(args.pop(0).strip())
		ret = self.tracking.centre_car(self.movement)
		if not ret:
			return
		if direction == "towards":
			self.movement.forward(distance)
		elif direction == "away":
			self.movement.backward(distance)


	def __init__(self):
		self.should_track = True
		self.script = ""
		self.stop = True
		self.movement = Movement()
		self.tracking = Tracking()
		self.continuous = False
		self.running = False
		self.commands = {
			"start": self.command_start,
			"move": self.command_move,
			"stop": self.command_stop,
			"centre": self.command_centre,
			"move_relative": self.command_move_relative,
		}

	def load_maneuver(self, maneuver):
		print("Loading maneuver")
		self.script = maneuver

	def set_is_continuous(self, setting):
		self.continuous = setting

	def execute_maneuver(self):
		self.running = True
		while 1:
			for line in self.script.split("\n"):
				args = line.split(" ")
				command = args.pop(0)
				try:
					self.commands[command.strip()](args)
				except KeyError:
					print("Unknown command {}".format(command.strip()))
					self.running = False
					exit(0)

	def start_maneuver(self):
		if self.running:
			return None
		self.stop = False
		print("Starting maneuver")	
		try:
			_thread.start_new_thread(self.execute_maneuver, ())
		except:
			print("Failed to start execute_maneuver thread")

	def stop_maneuver(self):
		print("Stopping maneuver")	
		self.stop = True