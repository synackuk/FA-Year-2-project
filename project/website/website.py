from flask import Flask
from flask import render_template
from flask import jsonify

manoeuvres = {"manoeuvre 1": "/api/set_manoeuvre/manoeuvre1",
			 "manoeuvre 2": "/api/set_manoeuvre/manoeuvre2"}

# creates a Flask application, named app
app = Flask(__name__)

# a route where we will display a welcome message via an HTML template

@app.route("/")
def homepage():
	return open("index.html", 'r').read()

@app.route("/<request>")
def get_page(request):
	return open(request, 'r').read()

@app.route("/api/get_manoeuvres")
def get_maneuvers():
	return jsonify(manoeuvres)


@app.route("/api/start")
def start_robot():
	print("Starting robot")
	return ""

@app.route("/api/stop")
def stop_robot():
	print("Stopping robot")
	return ""

@app.route("/api/set_manoeuvre/<request>")
def set_manoeuvre(request):
	print("Setting manoeuvre to \"%s\"." % request)
	return ""

# run the application
if __name__ == "__main__":
	app.run(debug=True)