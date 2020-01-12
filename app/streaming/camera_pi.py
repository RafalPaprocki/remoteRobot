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
        self.recording_path = "/home/pi/Desktop/remoteRobotVideos/"

    def start_recording(self, name):
        self.recoding_video_name = name
        if self.writer is None:
            frame = Camera.output.frame
            frame = Processing.to_np_array(frame)
            cv2.imwrite(self.recording_path + self.recoding_video_name + ".jpg", frame)
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')

            self.writer = cv2.VideoWriter(self.recording_path + self.recoding_video_name + ".avi",
                                          fourcc, 13, (640, 480), True)
            self.recording = True

    def stop_recording(self):
        self.recording = False

    def convert_to_mp4(self):
        cmds = ['ffmpeg', '-i', self.recording_path + self.recoding_video_name+".avi",
                self.recording_path + self.recoding_video_name + ".mp4"]
        subprocess.Popen(cmds)

    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()
            time.sleep(1.5)

    @classmethod
    def _thread(cls):
        with picamera.PiCamera(resolution='640x480', framerate=35) as camera:
            camera.video_stabilization = True
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
