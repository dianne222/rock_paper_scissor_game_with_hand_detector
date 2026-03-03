import cv2
import cvzone

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

while True:
    background_image = cv2.imread("images/background_image.png")

    success, image = capture.read()
    cv2.imshow("image", img)
    cv2.imshow("background", background_image)

    cv2.waitKey(1)