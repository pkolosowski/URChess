from EstimateChessboard import EstimateChessboard
import datetime
import imutils
import time
import cv2

from GameTracker import GameTracker
from Camera import Camera

class MotionDetection:

    def __display(self,roi,text="No Motion"):

        cv2.putText(roi, "Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        cv2.putText(roi, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, roi.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

        (h, w) = roi.shape[:2]
        center = (w / 2, h / 2)
        M = cv2.getRotationMatrix2D(center, 270, 1)
        roi = cv2.warpAffine(roi, M, (h, w))

        cv2.imshow("Motion Detection", roi)
        #cv2.imshow("Thresh", thresh)
        #cv2.imshow("Frame Delta", frameDelta)

    def __estimate_roi(self, corners):

        x_min = 1080
        x_max = 0
        y_min = 1920
        y_max = 0

        for corner in corners:
            if corner[1] < y_min:
                y_min = corner[1]
            if corner[1] > y_max:
                y_max = corner[1]
            if corner[0] < x_min:
                x_min = corner[0]
            if corner[0] > x_max:
                x_max = corner[0]

        return y_min, y_max, x_min, x_max

    def __process_image(self, image):

        image = imutils.resize(image, width=700, height=700)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.GaussianBlur(image, (21, 21), 0)

        return image

    def __move_detection(self,basic_frame, current_frame_copy, state, elapsed_time, previous_change,
                                      change_detected,start_time,move,change_counter, player_color,chessboard):

        if elapsed_time > 4:
            game_tracker = GameTracker()
            change_detected, move, state = game_tracker.track(player_color, basic_frame, current_frame_copy, state, chessboard)
            start_time = time.time()

        if change_detected == 0:
            elapsed_time = 0
            change_counter = 0

        if change_detected == 1 and previous_change == None:
            previous_change = move

        if change_detected == 1 and previous_change != None and previous_change == move:
            change_counter += 1

        if change_detected == 1 and previous_change != move and previous_change != None:
            change_counter = 0

        return change_detected, move, state, change_detected, previous_change, start_time, elapsed_time, change_counter

    def motion_detection(self, state, player_color,chessboard):

        change_counter = 0
        min_area = 2000
        elapsed_time = 0
        camera = Camera()
        previous_change = None
        basic_frame = camera.get_frame()
        previous_frame = camera.get_frame()

        corners = [chessboard["a1"], chessboard["a8"], chessboard["h1"], chessboard["h8"]]
        motion_flag = 0
        start_time = time.time()
        move = None
        change_detected = 0
        text = None
        while True:

            current_frame = camera.get_frame()
            current_frame_copy = current_frame.copy()
            y_min, y_max, x_min, x_max = self.__estimate_roi(corners)

            current_frame = current_frame[y_min - 40 : y_max + 40, x_min - 40 : x_max + 40]
            current_frame = self.__process_image(current_frame)
            previous_frame = previous_frame[y_min - 40: y_max + 40, x_min - 40: x_max + 40]
            previous_frame = self.__process_image(previous_frame)

            frameDelta = cv2.absdiff(previous_frame, current_frame)

            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            roi = current_frame_copy[y_min - 30: y_max + 30, x_min - 30: x_max + 30]
            roi = imutils.resize(roi, width=700, height=700)

            if motion_flag == 1:
                start_time = time.time()
                motion_flag = 0
            else:
                elapsed_time = time.time() - start_time

            for c in cnts:

                if cv2.contourArea(c) < min_area:
                    text = "No Motion"
                    continue
                else:
                    motion_flag = 1
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    text = "Motion Detected"

            self.__display(roi,text)
            change_detected, move, state, change_detected, previous_change, start_time, elapsed_time, change_counter = \
                self.__move_detection(basic_frame, current_frame_copy, state, elapsed_time, previous_change,
                                      change_detected, start_time,move, change_counter, player_color,chessboard)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or change_counter == 1:
                print move
                print state
                break

            previous_frame = current_frame_copy
        return move

