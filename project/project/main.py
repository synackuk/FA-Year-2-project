from flask import Flask
from flask import render_template
from flask import jsonify
import _thread
from time import sleep
import os
from os import listdir
from os.path import isfile, join
from manoeuvre_parser import Maneuver
from communication import Communication

ASSETS_PREFIX = "Site_Assets/"
MANOEUVRES_FOLDER_PREFIX = "manoeuvres/"

loaded_manoeuvre = ""

manoeuvre_parser = Maneuver()

communication = Communication(manoeuvre_parser)

app = Flask(__name__)

def clean_path(path):
	if "../" in path:
		return False
	return True

def get_site_asset(request):
	if not clean_path(request):
		return ""
	return "{}{}".format(ASSETS_PREFIX, request)

@app.route("/")
def homepage():
	return open(get_site_asset("index.html"), 'r').read()

@app.route("/<asset>")
def get_page(asset):
	try:
		return open(get_site_asset(asset), 'r').read()	
	except Exception:
		print("Failed to open file {}".format(asset))
		return ""

@app.route("/api/get_manoeuvres")
def get_maneuvers():
	print("Retrieveing list of manoeuvres.")
	manoeuvres = []
	for file in listdir(MANOEUVRES_FOLDER_PREFIX):
		if os.path.splitext(file)[1] == ".man":
			manoeuvres.append(os.path.splitext(file)[0])

	return jsonify(manoeuvres)


@app.route("/api/start")
def start_robot():
	global loaded_manoeuvre
	if not loaded_manoeuvre:
		return ""
	print("Starting robot")
	manoeuvre_parser.start_maneuver()
	return ""

@app.route("/api/stop")
def stop_robot():
	print("Stopping robot")
	manoeuvre_parser.stop_maneuver()
	return ""

@app.route("/api/set_continuous/<setting>")
def set_continuous(setting):
	if setting == "True":
		manoeuvre_parser.set_is_continuous(True)
	elif setting == "False":
		manoeuvre_parser.set_is_continuous(False)

	return ""

@app.route("/api/set_manoeuvre/<new_manoeuvre>")
def set_manoeuvre(new_manoeuvre):
	global loaded_manoeuvre
	if not clean_path(new_manoeuvre):
		return ""
	if manoeuvre_parser.running:
		return ""

	print("Setting manoeuvre to \"{}\".".format(new_manoeuvre))
	try:
		with open("{}{}.man".format(MANOEUVRES_FOLDER_PREFIX, new_manoeuvre), 'r') as f:
			loaded_manoeuvre = f.read()
			manoeuvre_parser.load_maneuver(loaded_manoeuvre)
	except:
		print("Manoeuvre {} doesn't exist.".format(new_manoeuvre))
	return ""

@app.route("/api/get_manoeuvre/")
def get_manoeuvre():
	print("Retrieveing current manoeuvre.")
	return loaded_manoeuvre

if __name__ == "__main__":
	if not communication.is_master():
		while True:
			try:
				communication.slave_wait_for_command()
			except Exception as e:
				print(e)
	communication.build_master_thread()
	app.run(debug=True, host="0.0.0.0")
