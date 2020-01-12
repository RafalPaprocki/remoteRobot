from app.models.video import Video
from app.streaming.camera_pi import Camera
from app.preprocessing.preprocessing import Processing
from flask import Response , request
from app import app, db
from flask import send_file
from app.preprocessing.lane_detection import LineDetection
from app.robot_control.robot_control import steering_with_angle
import cv2
import time
import subprocess

camera = Camera()
def gen():
    # p = Processing()
    # p.load()
    # line_detection = LineDetection()

    camera.initialize()

    # time_start = time.time()
    # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    # name = "fff.avi"
    # writer = cv2.VideoWriter("/home/pi/Desktop/" + name, fourcc, 13, (640, 480), True)
    while True:
            frame = camera.take_frame()

            # frame, steering_angle, lane_lines = line_detection.detect_lines(frame)
            # frame = p.draw_lane_lines(frame, detected_lines)
            # steering_with_angle(steering_angle, lane_lines)

            #
            # if time.time() - time_start < 30:
            #     writer.write(frame)
            #     print("writer")
            # elif writer is not None:
            #     writer.release()

            frame = Processing.to_jpeg(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video/convert/<fname>', methods=['GET'])
def video_convert(fname):
    cmds = ['ffmpeg', '-i', '/home/pi/Desktop/g.avi', fname + ".mp4"]
    subprocess.Popen(cmds)
    return Response(status=200)


@app.route('/video', methods=['POST'])
def video_save():
    data = request.get_json()
    v = Video(path='/home/pi/Desktop/remoteRobotVideos',
              name=data['videoname'] + '.mp4',
              preview_frame=data['videoname'] + '.jpg')
    db.session.add(v)
    db.session.commit()
    return Response(status=200)


@app.route('/video/recording/start/<fname>')
def video_start(fname):
    camera.start_recording(fname)
    return Response(status=200)


@app.route('/video/recording/stop')
def video_stop():
    camera.stop_recording()
    return Response(status=200)


@app.route('/file-download/<vid>')
def fg(vid):
    try:
        return send_file('/home/pi/Desktop/remoteRobotVideos/' + vid)
    except Exception as e:
        return str(e)

i = 102

@app.route('/photo')
def make_foto():
    img = camera.take_frame()
    cv2.imwrite('/home/pi/Desktop/imageSign2/img' + str(i) + '.jpg', img)
    global i
    i += 1
    return Response(status=200)