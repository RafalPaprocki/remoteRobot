from flask import render_template, request
from app import app, socketio
from flask_socketio import emit, join_room, leave_room


@app.route('/')
def index():
    return render_template('mainPage.html')


@app.route('/robot-config')
def robot_config():
    return render_template('video_preview.html')


@app.route('/robot-routes')
def robot_routes():
    return render_template('robotRoutes.html')


@app.route('/data-preview')
def data_preview():
    return render_template('dataPreview.html')


@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})
    print(clients)


@socketio.on('my broadcast event', namespace='/test')
def test_messagee(message):
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('join', namespace='/test')
def join_roome(data):
    room = "room1"
    join_room(room)
    x.start()


@socketio.on('leave', namespace="/test")
def leave_roome(data):
    room = "room1"
    leave_room(room)


clients = []


@socketio.on('connect', namespace='/test')
def connect():
    clients.append(request.remote_user)


@socketio.on('disconnect', namespace='/test')
def disconnect():
    clients.remove(request.remote_user)







