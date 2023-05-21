import cv2
import mediapipe as mp
import pyautogui

# Desativa a função de segurança do PyAutoGUI
pyautogui.FAILSAFE = False
# Inicializa a captura de vídeo da câmera
video = cv2.VideoCapture(0)
# Inicializa o modelo de detecção de mãos
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializa o módulo de desenho do Mediapipe
mpDraw = mp.solutions.drawing_utils

while True:
    # Lê o próximo quadro do vídeo
    success, img = video.read()
    # Inverte o eixo horizontal da imagem para corresponder a um espelho
    img = cv2.flip(img, 1)
    # Verifica se a leitura do quadro foi bem-sucedida
    if not success:
        break

    # Converte a imagem de BGR para RGB (necessário para o modelo de mãos)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processa a imagem em busca de mãos
    results = hands.process(imgRGB)
    # Obtém os pontos das mãos detectadas
    handPoints = results.multi_hand_landmarks
    # Obtém as dimensões da imagem
    h, w, _ = img.shape

    # Define as dimensões e posição do retângulo de referência
    rect_width = 288
    rect_height = 162
    rect_x = (w - rect_width) // 2
    rect_y = (h - rect_height) // 2 - 100
    # Desenha o retângulo de referência na imagem
    cv2.rectangle(img, (rect_x, rect_y), (rect_x + rect_width, rect_y + rect_height), (0, 0, 255), 2)

    # Verifica se foram detectadas mãos na imagem
    if handPoints:
        # Para cada mão detectada
        for points in handPoints:
            # Desenha os pontos da mão e as conexões entre eles na imagem
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)
            # Converte as coordenadas normalizadas para coordenadas de pixels
            points_list = []
            for id, cord in enumerate(points.landmark):
                cx, cy = int(cord.x * w), int(cord.y * h)
                points_list.append((cx, cy))

            # Verifica se foram encontrados pontos da mão
            if points_list:
                # Obtém as coordenadas da ponta do dedo indicador para verificar se o dedo indicador está dentro do retângulo de referência
                finger_index = points_list[8]
                if (rect_x < finger_index[0] < rect_x + rect_width and rect_y < finger_index[1] < rect_y + rect_height):
                    # Imprime uma mensagem indicando que a ponta do dedo indicador está dentro do retângulo
                    print("O dedo indicador está no retângulo vermelho")
                    # Verifica se o dedo indicador está levantado
                    if (points_list[8][1] < points_list[7][1] < points_list[6][1] < points_list[5][1]):
                        # Obtém as coordenadas do dedo indicador e converte para o espaço de um monitor FHD
                        x, y = finger_index
                        new_x = int(round((x - rect_x) * 6.67))
                        new_y = int(round((y - rect_y) * 6.67))
                        # Imprime as coordenadas nas diferentes referências
                        print("Coordenada no video da camera:   ", x, ",", y)
                        print("Coordenada no quadrado menor:    ", x - rect_x, ",", y - rect_y)
                        print("Coordenada menor convertida FHD: ", new_x, ",", new_y, "\n")
                        # Move o cursor do mouse para as novas coordenadas
                        pyautogui.moveTo(new_x, new_y)

    # Exibe a imagem com as anotações na janela e aguarda a tecla 'q' ser pressionada para encerrar o programa
    cv2.imshow("Air Mouse", img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Libera os recursos utilizados
video.release()
cv2.destroyAllWindows()
