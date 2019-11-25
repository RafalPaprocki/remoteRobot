import cv2
import numpy as np


class Processing:
    def __init__(self):
        self.net = None

    @staticmethod
    def to_jpeg(image):
        s, img = cv2.imencode(".jpeg", image)
        return img.tobytes()

    @staticmethod
    def to_np_array(image):
        img = cv2.imdecode(np.fromstring(image, dtype=np.uint8), 1)
        return img

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]

    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    def load(self):
        self.net = cv2.dnn.readNetFromCaffe("/home/pi/Desktop/MobileNetSSD_deploy.prototxt.txt", "/home/pi/Desktop/MobileNetSSD_deploy.caffemodel")

    def image_preprocess(self, image):
        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (200, 200)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.5:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # display the prediction
                label = "{}: {:.2f}%".format(self.CLASSES[idx], confidence * 100)
                print("[INFO] {}".format(label))
                cv2.rectangle(image, (startX, startY), (endX, endY),
                              self.COLORS[idx], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(image, label, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.COLORS[idx], 2)

        return image



