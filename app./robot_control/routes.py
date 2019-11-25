from app import app
from flask import render_template, request
import app.robot_control.robot_control as robot_control
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)


@app.route("/robot/back", methods=['GET'])
def robot_back():
    robot_control.back()
    return "ok"


@app.route("/robot/forward", methods=['GET'])
def robot_forward():
    robot_control.forward()
    return "ok"


@app.route("/robot/left", methods=['GET'])
def robot_left():
    robot_control.left()
    return "ok"


@app.route("/robot/right", methods=['GET'])
def robot_right():
    robot_control.right()
    return "ok"


@app.route("/robot/stop", methods=['GET'])
def robot_stop():
    robot_control.stop()
    return "ok"


@app.route("/robot/right_forward", methods=['GET'])
def robot_right_forward():
    robot_control.right_forward()

    return "ok"


@app.route("/robot/left_forward", methods=['GET'])
def robot_left_forward():
    robot_control.left_forward()
    return "ok"


@app.route("/robot/left_back", methods=['GET'])
def robot_left_back():
    robot_control.left_back()
    return "ok"


@app.route("/robot/right_back", methods=['GET'])
def robot_right_back():
    robot_control.right_back()
    return "ok"


@app.route("/robot/horizontal/move/<angle>", methods=['GET'])
def robot_horizontal_move(angle):
    kit.servo[4].angle = int(angle)
    return "ok"


@app.route("/robot/vertical/move/<angle>", methods=['GET'])
def robot_vertical_move(angle):
    kit.servo[3].angle = int(angle)
    return "ok"