import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
state_result = False
start_game = False
scores = [0, 0] # [AI score, Player score]

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

    if start_game:
        if state_result is False:
            timer = time.time() - initial_time
            cv2.putText(background_image, str(int(timer)),(605,435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                state_result = True
                timer = 0

                if hands:
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        player_move = "rock"
                    if fingers == [1, 1, 1, 1, 1]:
                        player_move = "paper"
                    if fingers == [0, 1, 1, 0, 0]:
                        player_move = "scissor"

                    random_number = random.randint(1, 3)
                    if random_number == 1:
                        ai_move = "paper"
                    if random_number == 2:
                        ai_move = "rock"
                    if random_number == 3:
                        ai_move = "scissor"
                    image_ai = cv2.imread(f'images/{ai_move}_image.png', cv2.IMREAD_UNCHANGED)
                    background_image = cvzone.overlayPNG(background_image, image_ai, (149, 310))

                    # Player Wins
                    if (player_move == "rock" and ai_move == "scissor") or \
                            (player_move == "paper" and ai_move == "rock") or \
                            (player_move == "scissor" and ai_move == "paper"):
                        scores[1] += 1

                    # AI Wins
                    if (ai_move == "rock" and player_move == "scissor") or \
                            (ai_move == "paper" and player_move == "rock") or \
                            (ai_move == "scissor" and player_move == "paper"):
                        scores[0] += 1

    background_image[233:653, 795:1195] = image_scaled

    if state_result:
        background_image = cvzone.overlayPNG(background_image, image_ai, (149, 310))

    cv2.putText(background_image, str(scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(background_image, str(scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(background_image, "Press 's' to play", (570, 150), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

    # cv2.imshow("Image", image)
    cv2.imshow("Background", background_image)
    # cv2.imshow("Scaled", image_scaled)

    key = cv2.waitKey(1)
    if key == ord('s'):
        start_game = True
        initial_time = time.time()
        state_result = False