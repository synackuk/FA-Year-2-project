class Maneuver:
	def __init__(self, forward, left, backward, right):
		self.script = ""
		self.stop = True
		self.forward = forward
		self.backward = forward
		self.left = forward
		self.right = forward

	def command_start(args):
		print("started maneuver")	

	def command_stop(args):
		print("stopped maneuver")	

	def command_move(args):
		direction = args.pop(0)
		distance = int(args.pop(0))
		print("Moving {} {} steps".format(direction, distance))	
		if direction == "forward":
			self.forward(distance)
		elif direction == "backward":
			self.backward(distance)
		elif direction == "left":
			self.left(distance)
		elif direction == "right":
			self.right(distance)

	commands = {
		"start": command_start,
		"move": command_move,
		"stop": command_stop
	}	

	def load_maneuver(self, maneuver):
			self.script = maneuver
		
	def start_maneuver(self):
		self.stop = False
		while not self.stop:
			for line in self.script.split("\n"):
				args = line.split(" ")
				command = args.pop(0)
				commands[command](args)

	def stop_maneuver(self):
		self.stop = True