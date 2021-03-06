import cv2
import numpy as np
import math


class LineDetection:
    def __init__(self):
        self.img_width = 640
        self.img_height = 320
        self.limit_img_for_lines = 4 / 9

    def mask_hsv(self, img):
        img = cv2.resize(img, (self.img_width, self.img_height))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        lower_red = np.array([175, 40, 10], dtype=np.uint8)
        upper_red = np.array([180, 255, 255], dtype=np.uint8)

        lower_red2 = np.array([0, 40, 10], dtype=np.uint8)
        upper_red2 = np.array([10, 255, 255], dtype=np.uint8)

        red_mask = cv2.inRange(hsv, lower_red, upper_red)
        red2_mask = cv2.inRange(hsv, lower_red2, upper_red2)

        mask = cv2.bitwise_or(red_mask, red2_mask)

        res = cv2.bitwise_and(img, img, mask=mask)

        return res

    def detect_edges(self, img):
        edges = cv2.Canny(img, 200, 400)

        height, width = edges.shape
        mask = np.zeros_like(edges)
        mask[int(height * self.limit_img_for_lines):height] = 255

        limited_edges = cv2.bitwise_and(edges, mask)

        return limited_edges

    def find_lanes(self, img, rho=3, min_threshold=40, minLineLength=10, maxLineGap=44):
        angle = np.pi / 180
        line_segments = cv2.HoughLinesP(img, rho, angle, min_threshold,
                                        np.array([]), minLineLength, maxLineGap)

        return line_segments

    def split_lines(self, line_segments):
        left_fit = []
        right_fit = []
        boundary = 1 / 3
        left_region_boundary = self.img_width * (1 - boundary)
        right_region_boundary = self.img_width * boundary

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

        return left_fit, right_fit

    def calc_lane_lines(self, left_fit, right_fit):
        lane_lines = []

        if len(left_fit) > 0:
            left_fit_average = np.average(left_fit, axis=0)
            lane_lines.append(self.make_points(left_fit_average))

        if len(right_fit) > 0:
            right_fit_average = np.average(right_fit, axis=0)
            d = self.make_points(right_fit_average)
            lane_lines.append(d)
        return lane_lines

    def calc_offset(self, lane_lines):
        x_offset, y_offset = None, None
        if len(lane_lines) == 2:
            _, _, left_x2, _ = lane_lines[0][0]
            _, _, right_x2, _ = lane_lines[1][0]
            mid = int(self.img_width / 2)
            x_offset = (left_x2 + right_x2) / 2 - mid
            y_offset = int(self.img_height / 2)

        elif len(lane_lines) == 1:
            x1, _, x2, _ = lane_lines[0][0]
            x_offset = x2 - x1
            y_offset = int(self.img_height / 2)

        return x_offset, y_offset

    def count_steering_angle(self, x_offset, y_offset):
        if x_offset is not None and y_offset is not None:
            angle_to_mid_radian = math.atan(x_offset / y_offset)
            angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)
            steering_angle = angle_to_mid_deg + 90
            print(steering_angle)
            return steering_angle

    def make_points(self, line):
        slope, intercept = line
        y1 = self.img_height
        y2 = int(y1 * self.limit_img_for_lines)

        x1 = max(-self.img_width, min(2 * self.img_width, int((y1 - intercept) / slope)))
        x2 = max(-self.img_width, min(2 * self.img_width, int((y2 - intercept) / slope)))

        return [[x1, y1, x2, y2]]

    def draw_lane_lines(self, frame, lines, line_color=(143, 255, 230), line_width=25):
        line_image = np.zeros_like(frame)
        if lines is not None:
            for line in lines:
                for x1, y1, x2, y2 in line:
                    cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
        line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
        return line_image

    def draw_sterring_line(self, img, steering_angle, line_color=(12, 215, 130), line_width=15):
        if steering_angle is not None:
            radian = steering_angle / 180.0 * math.pi
            y2 = int(self.img_height * self.limit_img_for_lines)
            y1 = int(self.img_height)
            x1 = int(self.img_width // 2)
            a = math.tan(radian)
            x2 = int((y2 - y1 + a * x1) // a)
            line_image = np.zeros_like(img)
            cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
            img = cv2.addWeighted(img, 0.8, line_image, 1, 1)
        return img

    def detect_lines(self, img):
        img = cv2.resize(img, (640, 320))
        img2 = self.mask_hsv(img)
        img3 = self.detect_edges(img2)
        line_segments = self.find_lanes(img3)
        left_fit, right_fit = self.split_lines(line_segments)
        lane_lines = self.calc_lane_lines(left_fit, right_fit)
        img4 = self.draw_lane_lines(img, lane_lines)
        x_offset, y_offset = self.calc_offset(lane_lines)
        steering_angle = self.count_steering_angle(x_offset, y_offset)
        img5 = self.draw_sterring_line(img4, steering_angle)

        return img5, steering_angle, lane_lines