import cv2
import mediapipe as mp
import pyautogui
import time


def dedo_polegar(points_list):
    if (points_list[4][0] < points_list[3][0]):
        return True
    else:
        return False

def dedo_indicador(points_list):
    if (points_list[8][1] < points_list[7][1] < points_list[6][1] < points_list[5][1]):
        return True
    else:
        return False


def dedo_medio(points_list):
    if (points_list[12][1] < points_list[11][1] < points_list[10][1] < points_list[9][1]):
        return True
    else:
        return False


def dedo_anelar(points_list):
    if (points_list[16][1] < points_list[15][1] < points_list[14][1] < points_list[13][1]):
        return True
    else:
        return False


def dedo_mindinho(points_list):
    if (points_list[20][1] < points_list[19][1] < points_list[18][1] < points_list[17][1]):
        return True
    else:
        return False

pyautogui.FAILSAFE = False
video = cv2.VideoCapture(0)
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils
last_click_time = time.time()

while True:
    success, img = video.read()
    img = cv2.flip(img, 1)  # Inverte o eixo da câmera
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

            if points_list:
                finger_index = points_list[8]  # Coordenadas do dedo indicador (ponta)
                if (rect_x < finger_index[0] < rect_x + rect_width and rect_y < finger_index[1] < rect_y + rect_height):
                    print("O dedo indicador está no retângulo vermelho")
                    if (dedo_indicador(points_list)):
                        if (dedo_mindinho(points_list)):
                            print("O dedo mindinho está levantado")
                            print(f"{last_click_time}")
                            current_time = time.time()
                            print(f"{current_time}")
                            if current_time - last_click_time >= 1.0:
                                print("Click realizado")
                                pyautogui.click()
                                last_click_time = current_time
                                print(f"{last_click_time}")
                                print(f"{current_time}")
                        x, y = finger_index
                        new_x = int(round((x - rect_x) * 6.67))
                        new_y = int(round((y - rect_y) * 6.67))
                        print("Coordenada no video da camera:   ", x, ",", y)
                        print("Coordenada no quadrado menor:    ", x - rect_x, ",", y - rect_y)
                        print("Coordenada menor convertida FHD: ", new_x, ",", new_y, "\n")
                        pyautogui.moveTo(new_x, new_y)

    cv2.imshow("Air Mouse", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
