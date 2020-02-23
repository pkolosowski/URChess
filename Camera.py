import cv2

class Camera:

    def __init__(self): #set camera resolution

        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    def get_frame(self):

        return_value, image = self.cap.read()
        return image
