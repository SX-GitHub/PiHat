import math
from flask import Flask, render_template, jsonify

app = Flask(__name__)

__PAN_ORIGIN = -135
__TILT_ORIGIN = 25
__PAN_MAX = 45
__TILT_MAX = 110

pan_position = __PAN_ORIGIN
tilt_position = __TILT_ORIGIN

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tilt/<radians>')
def tilt(radians):
    global tilt_position, pan_position
    degrees = math.degrees(float(radians))
    if tilt_position + degrees > __TILT_MAX:
        degrees = __TILT_MAX - tilt_position
    if tilt_position + degrees < __TILT_ORIGIN:
       degrees = __TILT_ORIGIN - tilt_position
    tilt_position += degrees
    # TODO: drive the SG90 servo to rotate to tilt_position

    return jsonify(actual = math.radians(degrees)), 200

@app.route('/pan/<radians>')
def pan(radians):
    global tilt_position, pan_position
    degrees = math.degrees(float(radians))
    if pan_position + degrees > __PAN_MAX:
        degrees = __PAN_MAX - pan_position
    if pan_position + degrees < __PAN_ORIGIN:
        degrees = __PAN_ORIGIN - pan_position
    pan_position += degrees
    # TODO: drive the MG90S servo to rotate to pan_position

    return jsonify(actual = math.radians(degrees)), 200
