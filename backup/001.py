# Usando o dedo indicador para mover e o mindinho para clicar

import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False

video = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = video.read()
    img = cv2.flip(img, 1)  # Inverte o eixo da camera
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    handPoints = results.multi_hand_landmarks

    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)
            points_list = []
            for id, cord in enumerate(points.landmark):
                h, w, _ = img.shape
                cx, cy = int(cord.x * w), int(cord.y * h)
                points_list.append((cx, cy))

            finger_ids = [8, 12, 16, 20]
            finger_count = 0

            if points_list:
                if points_list[4][0] < points_list[3][0]:
                    finger_count += 1
                for i in finger_ids:
                    if points_list[i][1] < points_list[i - 2][1]:
                        finger_count += 1

                # Usando a posição do dedo indicador para mover o cursor do mouse
                x, y = points_list[8][0], points_list[8][1]
                screenWidth, screenHeight = pyautogui.size()
                pyautogui.moveTo(x * screenWidth / w, y * screenHeight / h)

                # Verifica se o dedo mindinho ta levantado
                if points_list[20][1] < points_list[19][1] < points_list[18][1] < points_list[17][1]:
                    # Executa um clique com o mouse
                    pyautogui.click()

            cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)
            cv2.putText(img, str(finger_count), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)

    cv2.imshow('Imagem', img)

    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break

video.release()
cv2.destroyAllWindows()
