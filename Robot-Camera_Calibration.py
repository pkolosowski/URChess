import cv2
from Camera import Camera


class Calibration:

    def __init__(self):

        self.good_contours = []

    def filter_contours(self, contours): #selects contours with specified surface area


        for con in contours:
            area = cv2.contourArea(con)
            if 2000 < area < 4000:
                self.good_contours.append(con)

        return self.good_contours

    def obtain_image(self): #obtains and pre-process image from camera

        camera = Camera()
        img = camera.get_frame()
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 100, 255, 1)
        blur = cv2.medianBlur(thresh, 7)

        return blur, img

    def find_contours(self, blur): #finds contours storing all boundary points

        _,contours, hierarchy, = cv2.findContours(~blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        return contours

    def find_controids(self, good_contours, img): #draws boundary points of each contour,
        # calculates each contour centroid and prints it on image

        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        fontColor = (0, 255, 0)
        lineType = 2

        for j in range(0, len(good_contours)):

            max_x = 0
            min_x = 400000
            max_y = 0
            min_y = 400000

            for i in range(0, len(good_contours[j])):
                cv2.circle(img, (good_contours[j][i][0][0], good_contours[j][i][0][1]), 5, color=(0, 0, 255),
                           thickness=1)
                if good_contours[j][i][0][0] > max_x:
                    max_x = good_contours[j][i][0][0]
                if good_contours[j][i][0][0] < min_x:
                    min_x = good_contours[j][i][0][0]
                if good_contours[j][i][0][1] > max_y:
                    max_y = good_contours[j][i][0][1]
                if good_contours[j][i][0][1] < min_y:
                    min_y = good_contours[j][i][0][1]

            cx = (min_x + max_x) / 2
            cy = (min_y + max_y) / 2
            cv2.circle(img, (int(cx), int(cy)), 1, color=(0, 0, 255), thickness=3)
            print (int(cx), int(cy))
            cv2.putText(img, str(cx) + ' ' + str(cy), (int(cx), int(cy)), font, fontScale, fontColor, lineType)
            cv2.imwrite('calibration_markers.png', img)


calibration = Calibration()
blur, img = calibration.obtain_image()
contours = calibration.find_contours(blur)
contours_filtered = calibration.filter_contours(contours)
calibration.find_controids(contours_filtered, img)













