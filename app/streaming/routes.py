from app.streaming.camera_pi import Camera
from app.preprocessing.preprocessing import Processing
from flask import Response
from app import app


def gen():
    p = Processing()
    # p.load()
    camera = Camera()
    camera.initialize()
    i = 0
    while True:
            frame = camera.take_frame()
            frame = Processing.to_np_array(frame)
            # frame, detected_lines = p.line_detect(frame)
            # frame = p.draw_lane_lines(frame, detected_lines)
            i += 1
            frame = Processing.to_jpeg(frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_stream')
def video_stream():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')