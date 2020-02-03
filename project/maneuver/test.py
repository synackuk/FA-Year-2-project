def command_start(args):
	print("started maneuver")

def command_stop(args):
	print("stopped maneuver")

def command_move(args):
	direction = args.pop(0)
	distance = int(args.pop(0))
	print("Moving {} {} steps".format(direction, distance))

def command_rotate(args):
	direction = args.pop(0)
	print("Rotating {}".format(direction))

commands = {
	"start": command_start,
	"move": command_move,
	"rotate": command_rotate,
	"stop": command_stop
}

maneuver_file = "maneuver1.man"
script = ""
with open(maneuver_file) as f:
	script = f.read()

for line in script.split("\n"):
	args = line.split(" ")
	command = args.pop(0)
	commands[command](args)