from app import app
from flask import Response
import app.robot_control.robot_control as robot_control


@app.route("/robot/back", methods=['GET'])
def robot_back():
    robot_control.back()
    return Response(status=200)


@app.route("/robot/forward", methods=['GET'])
def robot_forward():
    robot_control.forward()
    return Response(status=200)


@app.route("/robot/left", methods=['GET'])
def robot_left():
    robot_control.left()
    return Response(status=200)


@app.route("/robot/right", methods=['GET'])
def robot_right():
    robot_control.right()
    return Response(status=200)


@app.route("/robot/stop", methods=['GET'])
def robot_stop():
    robot_control.stop()
    return Response(status=200)


@app.route("/robot/right_forward", methods=['GET'])
def robot_right_forward():
    robot_control.right_forward()
    return Response(status=200)


@app.route("/robot/left_forward", methods=['GET'])
def robot_left_forward():
    robot_control.left_forward()
    return Response(status=200)


@app.route("/robot/left_back", methods=['GET'])
def robot_left_back():
    robot_control.left_back()
    return Response(status=200)


@app.route("/robot/right_back", methods=['GET'])
def robot_right_back():
    robot_control.right_back()
    return Response(status=200)


@app.route("/robot/horizontal/move/<angle>", methods=['GET'])
def robot_horizontal_move(angle):
    robot_control.servo_move(3, angle)
    return Response(status=200)


@app.route("/robot/vertical/move/<angle>", methods=['GET'])
def robot_vertical_move(angle):
    robot_control.servo_move(4, angle)
    return Response(status=200)