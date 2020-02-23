import cv2
import numpy as np

class EstimateChessboard:

    def __get_item(self, item):
        return item[0]

    def __get_item2(self, item):
        return item[1]

    def __get_feature_points(self, img):

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (7, 7))
        corners2 = cv2.cornerSubPix(gray, corners, (7, 7), (-1, -1), criteria)
        cv2.drawChessboardCorners(img,(7,7),corners2,ret)
        cv2.imwrite("corners.png",img)

        return corners, corners2

    def __define_chessboard_orientation(self, dist):

        if abs(dist[0]) > abs(dist[1]):
            orientation = "horizontal"
        else:
            orientation = "vertical"

        return orientation

    def __assign_fields(self, orientation, positions):

        chessboard = {}

        if orientation == "horizontal":

            for i in range (0, 8):
                output = sorted(positions[i], key=self.__get_item)
                letter = chr(104 - i)
                for j in range (8, 0,-1):
                    chessboard["%s%s" % (letter, 8-j+1)] = output[j-1]

        if orientation == "vertical":
            for i in range (0, 8):
                output = sorted(positions[i], key=self.__get_item2, reverse=True)
                for j in range (0, 8):
                    letter = chr(97 + j)
                    chessboard["%s%s" % (letter, i+1)] = output[j]

        return chessboard

    def __print_centers(self, chessboard, img):

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.3

        for key, value in chessboard.items():
            cv2.putText(img, key, value, font, fontScale, (0, 255, 0))
            cv2.circle(img, value, 1, (0, 0, 255), 2)

        cv2.imwrite('estymacja_szachownica.png',img)

    def __calculate_centerpoints(self, corners2, img):

        centers = []

        for i in range(0,6):
            for j in range (0,6):
                p_1 = corners2[i*7+j][0]
                p_2 = corners2[i*7+j+1][0]
                p_3 = corners2[(i+1)*7+j][0]
                p_4 = corners2[(i+1)*7+j+1][0]
                center_point = ((p_1[0]+p_2[0]+p_3[0]+p_4[0])/4, (p_1[1]+p_2[1]+p_3[1]+p_4[1])/4)
                center_point = (int(center_point[0]), int(center_point[1]))
                centers.append(center_point)
                cv2.circle(img,center_point,1,(0,255,0),1)

        return centers, img

    def __calculate_borderpoints(self, centers):

        positions = []

        for i in range(0, 6):
            vector = centers[0+i*6:6+i*6]
            dist_11 = (centers[0+i*6][0] - centers[1+i*6][0], centers[0+i*6][1] - centers[1+i*6][1])
            dist_12 = (centers[5+i*6][0] - centers[4+i*6][0], centers[5+i*6][1] - centers[4+i*6][1])
            vector.insert(0, (centers[0+i*6][0] + dist_11[0], centers[0+i*6][1] + dist_11[1]))
            vector.append((centers[5+i*6][0] + dist_12[0], centers[5+i*6][1] + dist_12[1]))
            positions.append(vector)

        vector_0 = []
        vector_7 = []

        for i in range(0, 8):

            dist = (positions[0][i][0] - positions[1][i][0], positions[0][i][1] - positions[1][i][1])
            vector_0.append((positions[0][i][0] + dist[0], positions[0][i][1] + dist[1]))
            dist = (positions[5][i][0] - positions[4][i][0], positions[5][i][1] - positions[4][i][1])
            vector_7.append((positions[5][i][0] + dist[0], positions[5][i][1] + dist[1]))

        positions.insert(0,vector_0)
        positions.append(vector_7)

        return positions

    def __calculate_line_equations(self, positions):

        line_equations = []

        for i in range (0, 8):
            a = float((positions[i][0][1] - -1*positions[i][7][1] )) / float( positions[i][0][0] - -1*positions[i][7][0])
            b = positions[i][0][1] - a*positions[i][0][0]
            line_equations.append((a,b))

        return line_equations

    def __estimate_borders(self, orientation, positions,line_equations):

        if orientation == "horizontal":
            for i in range(0, 7):
                for j in range(1+i, 8):
                    if line_equations[i][1] > line_equations[j][1]:

                        temp = line_equations[i]
                        line_equations[i] = line_equations[j]
                        line_equations[j] = temp
                       # print i,j
                        temp = positions[i]
                        positions[i] = positions[j]
                        positions[j] = temp

        if orientation == "vertical":
            for i in range(0, 7):
                for j in range (1+i,8):
                    if positions[i][3][0] < positions[j][3][0]:
                        temp = positions[i]
                        positions[i] = positions[j]
                        positions[j] = temp

        return positions

    def estimate_chessboard_postion(self, img):

        corners, corners2 = self.__get_feature_points(img)
        dist = corners2[0][0] - corners[1][0]
        orientation = self.__define_chessboard_orientation(dist)
        centers, img = self.__calculate_centerpoints(corners2, img)
        positions = self.__calculate_borderpoints(centers)
        line_equations = self.__calculate_line_equations(positions)
        positions = self.__estimate_borders(orientation, positions, line_equations)
        chessboard = self.__assign_fields(orientation, positions)
        self.__print_centers(chessboard, img)

        return chessboard

