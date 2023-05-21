import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = False
video = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils

while True:
    success, img = video.read()
    img = cv2.flip(img, 1)
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

            # Exibindo quantidade de dedos levantados
            cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)
            cv2.putText(img, str(finger_count), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)
            # Verificando se o indicador está dentro do triangulo vermelho
            if points_list:
                finger_index = points_list[8]  # Coordenadas do dedo indicador (ponta)
                if rect_x < finger_index[0] < rect_x + rect_width and rect_y < finger_index[1] < rect_y + rect_height:
                    print("O dedo indicador está dentro do retângulo vermelho!")

    # Exibindo retangulo vermelho
    h, w, _ = img.shape
    rect_width = 288 # ((1920/10) *1.5)
    rect_height = 162
    rect_x = (w - rect_width) // 2
    rect_y = (h - rect_height) // 2 - 100
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

    cv2.imshow('Imagem', img)

    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break

video.release()
cv2.destroyAllWindows()
