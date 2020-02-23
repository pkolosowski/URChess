import cv2
import numpy as np
from EstimateChessboard import EstimateChessboard

class PieceDetection:

    def __init__(self):

        self.lower_red1 = np.array([0,100, 80])
        self.upper_red1 = np.array([30,255,255])

        self.lower_red2 = np.array([150, 100, 80])
        self.upper_red2 = np.array([180, 255, 255])

        self.lower_green = np.array([60, 100, 50])
        self.upper_green = np.array([90, 255, 170])

    def __hsv_filtration(self, img, color):

        img_hsv = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2HSV)

        if color == "red":
            mask0 = cv2.inRange(img_hsv.copy(), self.lower_red1, self.upper_red1)
            mask1 = cv2.inRange(img_hsv.copy(), self.lower_red2, self.upper_red2)
            mask = mask0 + mask1

        if color == "green":
            mask = cv2.inRange(img_hsv, self.lower_green, self.upper_green)

        filtered = cv2.bitwise_and(img.copy(), img.copy(), mask=mask)

        return mask, filtered

    def __blob_area_filtration(self, mask, min_area, max_area):

        conts, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        good_contours = []

        for con in conts:
            area = cv2.contourArea(con)
            if min_area < area < max_area:
                good_contours.append(con)

        return good_contours

    def __detect_pieces(self, filtered_red, filtered_green, chessboard):

        red_occupied = []
        green_occupied = []
        green_unoccupied = []
        red_unoccupied = []

        for field, coords in chessboard.items():

            x = coords[1]
            y = coords[0]

            red_counter = 0
            green_counter = 0

            for i in range(x - 5, x + 5):
                for j in range(y - 5, y + 5):
                    if filtered_red[i][j][0] != 0 and filtered_red[i][j][1] != 0 and filtered_red[i][j][2] != 0:
                        red_counter += 1
                    if filtered_green[i][j][0] != 0 and filtered_green[i][j][1] != 0 and filtered_green[i][j][2] != 0:
                        green_counter += 1

            if red_counter > 8:
                cv2.circle(filtered_red, (y, x), 1, (255, 0, 0), 1)
                red_occupied.append(field)
            else:
                red_unoccupied.append(field)
            if green_counter > 20:
                cv2.circle(filtered_green, (y, x), 3, (255, 0, 0), 1)
                green_occupied.append(field)
            else:
                green_unoccupied.append(field)

        cv2.imwrite("red.png", filtered_red)
        cv2.imwrite("green.png", filtered_green)

        return green_occupied, green_unoccupied, red_occupied, red_unoccupied

    def print_board(self, green_occupied, red_occupied):

        string = ""

        for i in range(8, 0, -1):
            for j in range(0, 8):
                if chr(97 + j) + str(i) in green_occupied:
                    string += "G"
                elif chr(97 + j) + str(i) in red_occupied:
                    string += "R"
                else:
                    string += '.'
            string += '\n'

        return string

    def get_chessboard_status(self, img, chessboard):

        mask_red, filtered_red = self.__hsv_filtration(img, "red")
        mask_green, filtered_green = self.__hsv_filtration(img, "green")

        good_contours_red = self.__blob_area_filtration(mask_red, 20, 500)
        good_contours_green = self.__blob_area_filtration(mask_green, 100, 500)

        green_occupied, green_unoccupied, red_occupied, red_unoccupied \
            = self.__detect_pieces(filtered_red, filtered_green, chessboard)


        return green_occupied, green_unoccupied, red_occupied, red_unoccupied

