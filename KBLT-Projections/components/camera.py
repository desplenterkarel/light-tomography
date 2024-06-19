from logger import LOGGER
import cv2 as cv




class Camera:
    def __init__(self, url):
        self.cap = cv.VideoCapture(url)
        LOGGER.debug("Camera Initialized")

    def get_ret_frame(self):
        return self.cap.read()

    def clean(self):
        cv.destroyAllWindows()
        self.cap.release()



