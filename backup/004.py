import screeninfo
import cv2
import mediapipe as mp
import pyautogui

# Obtém informações sobre os monitores conectados
monitors = screeninfo.get_monitors()
# Imprime as informações de cada monitor
print(f"Lista:\n{monitors}\n\nLista:")
# Imprime as informações de cada monitor
for monitor in monitors:
    print(monitor)
print("")
# Imprime as informações de cada monitor
for i, monitor in enumerate(monitors, 1):
    print(f"Monitor {i}:")
    print(f"\t- Largura: {monitor.width}")
    print(f"\t- Altura: {monitor.height}")
    print(f"\t- Posição à esquerda: {monitor.x}")
    print(f"\t- Posição ao topo: {monitor.y}")

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

    h, w, _ = img.shape
    rect_width = 288
    rect_height = 162
    rect_x = (w - rect_width) // 2
    rect_y = (h - rect_height) // 2 - 100
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)



    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)
            points_list = []
            for id, cord in enumerate(points.landmark):
                h, w, _ = img.shape
                cx, cy = int(cord.x * w), int(cord.y * h)
                points_list.append((cx, cy))
                # Verificando se o indicador está dentro do triangulo vermelho
            if points_list:
                finger_index = points_list[8]  # Coordenadas do dedo indicador (ponta)
                if rect_x < finger_index[0] < rect_x + rect_width and rect_y < finger_index[1] < rect_y + rect_height:
                    print("O dedo indicador está no retangulo vermelho")
                    x, y = points_list[8][0], points_list[8][1]
                    screenWidth, screenHeight = pyautogui.size()
                    x_corrected = int(x * screenWidth / w)
                    y_corrected = int(y * screenHeight / h)
                    x_new = x - rect_x
                    print(x_new)
                    new_x = x_new * 6.67
                    new_x_arredondado = round(new_x, 0)
                    new_x = int(new_x_arredondado)
                    y_new = y - rect_y
                    print(y_new)
                    new_y = y_new * 6.67
                    new_y_arredondado = round(new_y, 0)
                    new_y = int(new_y_arredondado)
                    print(x_corrected, ",", y_corrected)
                    print(x_corrected - rect_x, ",", y_corrected - rect_y)
                    print(new_x, ",", new_y)
                    pyautogui.moveTo(new_x, new_y)


    cv2.imshow('Hand Gesture Detector', img)
    key = cv2.waitKey(1)
    if key == 81 or key == 113:
        break

video.release()
cv2.destroyAllWindows()
