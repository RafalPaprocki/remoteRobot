import time
import io
import threading
import picamera
from threading import Condition
import cv2
import time
import subprocess

from app.preprocessing.preprocessing import Processing


class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            self.frame = self.buffer.getvalue()
            self.buffer.seek(0)
        return self.buffer.write(buf)


class Camera(object):
    thread = None
    frame = None
    output = StreamingOutput()


    def __init__(self):
        self.recording = False
        self.writer = None
        self.recoding_video_name = None

    def start_recording(self, name):
        self.recoding_video_name = name
        if self.writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            self.writer = cv2.VideoWriter("/home/pi/Desktop/" + self.recoding_video_name + ".avi", fourcc, 13, (640, 320), True)
            self.recording = True

    def stop_recording(self):
        self.recording = False

    def convert_to_mp4(self):
        cmds = ['ffmpeg', '-i', '/home/pi/Desktop/' + self.recoding_video_name+".avi", self.recoding_video_name + ".mp4"]
        subprocess.Popen(cmds)

    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            time.sleep(1.5)

    @classmethod
    def _thread(cls):
        with picamera.PiCamera(resolution='640x320', framerate=44) as camera:
            Camera.output = StreamingOutput()
            camera.start_recording(cls.output, format='mjpeg')
            time.sleep(100000000)

    def take_frame(self):
        frame = Camera.output.frame
        frame = Processing.to_np_array(frame)
        if self.writer is not None:
            if self.recording is True:
                self.writer.write(frame)
            else:
                self.writer.release()
                self.convert_to_mp4()
                self.recoding_video_name = None
                self.writer = None

        return frame
