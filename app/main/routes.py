from flask import render_template, request
from app import app, socketio, db
from flask_socketio import emit, join_room, leave_room
from sqlalchemy import desc
from app.models.video import Video
from flask_login import login_required

@app.route('/')
@login_required
def index():
    return render_template('mainPage.html')


@app.route('/video-preview')
@login_required
def video_preview():
    videos = Video.query.order_by(desc(Video.date)).all()
    return render_template('video_preview.html', videos = videos)


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







