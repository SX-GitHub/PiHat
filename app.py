import math
from time import sleep
from flask import Flask, render_template, jsonify

app = Flask(__name__)

__PAN_ORIGIN = -135
__TILT_ORIGIN = 25
__PAN_MAX = 45
__TILT_MAX = 110

pan_position = __PAN_ORIGIN
tilt_position = __TILT_ORIGIN

@app.context_processor
def export_global_variables():
    return dict(pan_position=pan_position, tilt_position=tilt_position, __PAN_ORIGIN=__PAN_ORIGIN, __TILT_ORIGIN=__TILT_ORIGIN)

def drive_tilt_servo(degrees):
    global tilt_position, pan_position
    if tilt_position + degrees > __TILT_MAX:
        degrees = __TILT_MAX - tilt_position
    if tilt_position + degrees < __TILT_ORIGIN:
       degrees = __TILT_ORIGIN - tilt_position    
    tilt_position += degrees
    # TODO: drive the SG90 servo to rotate to tilt_position. No need for translation.
    sleep(0.01)
    return degrees

def drive_pan_servo(degrees):
    global tilt_position, pan_position
    if pan_position + degrees > __PAN_MAX:
        degrees = __PAN_MAX - pan_position
    if pan_position + degrees < __PAN_ORIGIN:
        degrees = __PAN_ORIGIN - pan_position    
    pan_position += degrees
    servo_position = pan_position - __PAN_ORIGIN # MG90S postion 0° is -135° in the 3D model. 
    # TODO: drive the MG90S servo to rotate to pan_position
    sleep(0.01)
    return degrees

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tilt/<radians>')
def tilt(radians):
    global tilt_position, pan_position
    degrees = math.degrees(float(radians))
    actual = drive_tilt_servo(degrees)
    return jsonify(actual = math.radians(actual), pan = math.radians(pan_position), tilt = math.radians(tilt_position)), 200

@app.route('/pan/<radians>')
def pan(radians):
    global tilt_position, pan_position
    degrees = math.degrees(float(radians))
    actual = drive_pan_servo(degrees)
    return jsonify(actual = math.radians(actual), pan = math.radians(pan_position), tilt = math.radians(tilt_position)), 200
