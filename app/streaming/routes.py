from app.streaming.camera_pi import Camera
from app.preprocessing.preprocessing import Processing
from flask import Response
from app import app
from flask import send_file

def gen():
    # p = Processing()
    # p.load()
    camera = Camera()
    camera.initialize()

    while True:
            frame = camera.take_frame()
            frame = Processing.to_np_array(frame)
            # frame, detected_lines = p.line_detect(frame)
            # frame = p.draw_lane_lines(frame, detected_lines)
            frame = Processing.to_jpeg(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/file-download')
def fg():
    try:
        return send_file('/home/pi/Desktop/WIN_20191111_19_41_09_Pro.mp4')
    except Exception as e:
        return str(e)