import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import math
class Processing():

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

    @staticmethod
    def add_circle(image):
        cv2.circle(image, (500, 350), 20, (255, 0, 0), -1)
        return image

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

    def line_detect(self, img):
        img = cv2.resize(img, (640, 320))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_red = np.array([175, 40, 10], dtype=np.uint8)
        upper_red = np.array([180, 255, 255], dtype=np.uint8)

        lower_red2 = np.array([0, 40, 10], dtype=np.uint8)
        upper_red2 = np.array([10, 255, 255], dtype=np.uint8)

        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        red2_mask = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = cv2.bitwise_or(red_mask, red2_mask)

        res = cv2.bitwise_and(img, img, mask=mask)
        edges = cv2.Canny(res, 200, 400)

        height, width = edges.shape
        mask = np.zeros_like(edges)
        mask[height*5//9:height] = 255

        limited_edges = cv2.bitwise_and(edges, mask)
        rho = 3  # distance precision in pixel, i.e. 1 pixel
        angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
        min_threshold = 40  # minimal of votes
        line_segments = cv2.HoughLinesP(limited_edges, rho, angle, min_threshold,
                                        np.array([]), minLineLength=10, maxLineGap=44)






        lane_lines = []
        height, width, _ = img.shape
        left_fit = []
        right_fit = []

        boundary = 1 / 3
        left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
        right_region_boundary = width * boundary  # right lane line segment should be on left 2/3 of the screen

        if line_segments is not None:
            for line_segment in line_segments:
                for x1, y1, x2, y2 in line_segment:
                    fit = np.polyfit((x1, x2), (y1, y2), 1)
                    slope = fit[0]
                    intercept = fit[1]
                    if slope < 0:
                        if x1 < left_region_boundary and x2 < left_region_boundary:
                            left_fit.append((slope, intercept))
                    else:
                        if x1 > right_region_boundary and x2 > right_region_boundary:
                            right_fit.append((slope, intercept))

        left_fit_average = np.average(left_fit, axis=0)
        if len(left_fit) > 0:
            lane_lines.append(self.make_points(img, left_fit_average))
        # print(lane_lines)
        right_fit_average = np.average(right_fit, axis=0)
        d = None


        if len(right_fit) > 0:
            d = self.make_points(img, right_fit_average)
            lane_lines.append(d)

        if len(lane_lines) == 2:
            _, _, left_x2, _ = lane_lines[0][0]
            _, _, right_x2, _ = lane_lines[1][0]
            mid = int(width / 2)
            x_offset = (left_x2 + right_x2) / 2 - mid
            y_offset = int(height / 2)

        elif len(lane_lines) == 1:
            x1, _, x2, _ = lane_lines[0][0]
            x_offset = x2 - x1
            y_offset = int(height / 2)

        if len(lane_lines) > 0:
            angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
            angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
            steering_angle = angle_to_mid_deg + 90
            print(steering_angle)

        if len(lane_lines) == 2:
            print("2lines")

        # if len(lane_lines) > 1:
        #
        #     if steering_angle < 70:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.HIGH)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.LOW)
        #
        #         # GPIO.output(13, GPIO.LOW)
        #         # GPIO.output(6, GPIO.LOW)
        #         # GPIO.output(19, GPIO.LOW)
        #         # GPIO.output(26, GPIO.LOW)
        #     elif steering_angle < 115:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.HIGH)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.HIGH)
        #
        #     elif steering_angle < 170:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.LOW)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.HIGH)
        #
        #         # GPIO.output(13, GPIO.LOW)
        #         # GPIO.output(6, GPIO.LOW)
        #         # GPIO.output(19, GPIO.LOW)
        #         # GPIO.output(26, GPIO.LOW)
        #
        #
        #     else:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.LOW)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.LOW)

        # if len(lane_lines) == 1:
        #     x1, y1, x2, y2 = lane_lines[0][0]
        #     print("x1: " + str(x1))
        #
        #     if x1 < 580:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.HIGH)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.LOW)
        #         time.sleep(0.1)
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.LOW)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.LOW)
        #
        #     else:
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.HIGH)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.HIGH)
        #         time.sleep(0.1)
        #         GPIO.output(13, GPIO.LOW)
        #         GPIO.output(6, GPIO.LOW)
        #         GPIO.output(5, GPIO.LOW)
        #         GPIO.output(26, GPIO.LOW)

        #
        # if len(lane_lines) == 0 or lane_lines is None:
        #     GPIO.output(13, GPIO.LOW)
        #     GPIO.output(6, GPIO.LOW)
        #     GPIO.output(5, GPIO.LOW)
        #     GPIO.output(26, GPIO.LOW)
        return img, lane_lines

    def make_points(self, frame, line):
        height, width, _ = frame.shape
        slope, intercept = line
        y1 = height  # bottom of the frame
        y2 = int(y1 * 5 / 9)  # make points from middle of the frame down

        # bound the coordinates within the frame
        x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
        x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))

        return [[x1, y1, x2, y2]]

    def draw_lane_lines(self, frame, lines, line_color=(0, 255, 0), line_width=25):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image