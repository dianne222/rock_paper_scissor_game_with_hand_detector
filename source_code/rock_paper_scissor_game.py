import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

detector = HandDetector(maxHands=1)

while True:
    background_image = cv2.imread("images/background_image.png")
    success, image = capture.read()

    if not success:
        print("failed to read camera")
        break

    image_scaled = cv2.resize(image, (0, 0), None, 0.875, 0.875)
    image_scaled = image_scaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(image_scaled, draw=True, flipType=True)

    background_image[233:653, 795:1195] = image_scaled

    cv2.imshow("Image", image)
    cv2.imshow("Background", background_image)
    cv2.imshow("Scaled", image_scaled)

    cv2.waitKey(1)