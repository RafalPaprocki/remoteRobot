import cv2
import numpy as np


class Processing():
    @staticmethod
    def to_jpeg(image):
        s, img = cv2.imencode(".jpeg", image)
        return img.tobytes()

    @staticmethod
    def to_np_array(image):
        img = cv2.imdecode(np.fromstring(image, dtype=np.uint8), 1)
        return img

    @staticmethod
    def add_circle(image):
        cv2.circle(image, (500, 350), 20, (255, 0, 0), -1)
        return image