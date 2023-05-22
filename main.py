import cv2
import mediapipe as mp
import pyautogui
import time
import screeninfo
import psutil


def is_thumb_extended(points_list):
    return points_list[4][0] < points_list[3][0]


def is_index_finger_extended(points_list):
    return points_list[8][1] < points_list[7][1] < points_list[6][1] < points_list[5][1]


def is_middle_finger_extended(points_list):
    return points_list[12][1] < points_list[11][1] < points_list[10][1] < points_list[9][1]


def is_ring_finger_extended(points_list):
    return points_list[16][1] < points_list[15][1] < points_list[14][1] < points_list[13][1]


def is_pinky_finger_extended(points_list):
    return points_list[20][1] < points_list[19][1] < points_list[18][1] < points_list[17][1]


pyautogui.FAILSAFE = False
video = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(
    max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils
last_click_time = time.time()
# Obtém informações sobre os monitores conectados
monitors = screeninfo.get_monitors()
monitor_width = int(monitors[0].width)
rect_width = int(round(monitor_width * 0.15))
monitor_height = int(monitors[0].height)
rect_height = int(round(monitor_height * 0.15))

while True:
    success, img = video.read()
    img = cv2.flip(img, 1)  # Inverte o eixo da câmera
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    handPoints = results.multi_hand_landmarks

    h, w, _ = img.shape
    rect_x = (w - rect_width) // 2
    rect_y = (h - rect_height) // 2 - 100
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

    # Obtém o uso de memória atual do programa em MB
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024
    memory_text = f"RAM: {memory_usage:.2f} MB"  # Texto a ser exibido

    # Define a posição e o estilo do texto
    text_position = (rect_x + rect_width - 200, rect_y - 20)
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    color = (255, 255, 255)  # Cor do texto (branco)
    thickness = 2

    # Desenha o texto na imagem
    cv2.putText(img, memory_text, text_position, font, font_scale, color, thickness, cv2.LINE_AA)

    if handPoints:
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)
            points_list = [(int(cord.x * w), int(cord.y * h)) for cord in points.landmark]

            if points_list:
                finger_index = points_list[8]
                if (rect_x < finger_index[0] < rect_x + rect_width and rect_y < finger_index[1] < rect_y + rect_height):
                    if is_index_finger_extended(points_list) and is_pinky_finger_extended(points_list):
                        current_time = time.time()
                        if current_time - last_click_time >= 1.0:
                            pyautogui.click()
                            last_click_time = current_time
                    x, y = finger_index
                    new_x = int(round((x - rect_x) * 6.67))
                    new_y = int(round((y - rect_y) * 6.67))
                    pyautogui.moveTo(new_x, new_y)

    cv2.imshow("Air Mouse", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
