from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

# define the 0-9 digits with seven segment digits logic
DIGITS_LOOKUP = {
    (1, 1, 1, 0, 1, 1, 1): 0,
    (0, 0, 1, 0, 0, 1, 0): 1,
            (1, 0, 1, 1, 1, 1, 0): 2,
                (1, 0, 1, 1, 0, 1, 1): 3,
                    (0, 1, 1, 1, 0, 1, 0): 4,
                        (1, 1, 0, 1, 0, 1, 1): 5,
                            (1, 1, 0, 1, 1, 1, 1): 6,
                                (1, 0, 1, 0, 0, 1, 0): 7,
                                    (1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9
}

image = cv2.imread("WhatsApp1.jpeg")

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray", gray)

