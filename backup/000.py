import cv2  # Importa a biblioteca OpenCV para processamento de imagens
import mediapipe as mp  # Importa a biblioteca MediaPipe para detecção de mãos
import pyautogui  # Importa a biblioteca PyAutoGUI para controle do mouse
pyautogui.FAILSAFE = False  # Desativa a funcionalidade de segurança do PyAutoGUI

video = cv2.VideoCapture(0)  # Inicializa o objeto de captura de vídeo usando a câmera padrão
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5) # Inicializa o objeto "hands" para detecção de mãos, configurando a quantidade máxima de mãos, confiança mínima de detecção e confiança mínima de rastreamento
mpDraw = mp.solutions.drawing_utils  # Utilitários de desenho do MediaPipe

while True:  # Loop infinito para processar cada frame do vídeo
    success, img = video.read()  # Lê o próximo frame do vídeo
    img = cv2.flip(img, 1)  # Inverte o frame horizontalmente (espelha) para uma visualização mais intuitiva
    if not success:  # Verifica se a leitura do frame foi bem-sucedida
        break  # Se não for, sai do loop

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Converte o frame de BGR para RGB (formato usado pelo MediaPipe)
    results = hands.process(imgRGB)  # Processa o frame e obtém os resultados da detecção de mãos
    handPoints = results.multi_hand_landmarks  # Obtém as coordenadas dos pontos de referência das mãos

    if handPoints:  # Verifica se foram detectadas mãos no frame
        for points in handPoints:  # Itera sobre as mãos detectadas
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS) # Desenha os pontos de referência e as conexões entre eles no frame
            points_list = []
            for id, cord in enumerate(points.landmark):  # Itera sobre os pontos de referência da mão
                h, w, _ = img.shape  # Obtém a altura e largura do frame
                cx, cy = int(cord.x * w), int(cord.y * h)  # Converte as coordenadas normalizadas para pixels
                points_list.append((cx, cy))  # Adiciona as coordenadas do ponto à lista

            finger_ids = [8, 12, 16, 20]  # Índices dos pontos de referência das pontas dos dedos
            finger_count = 0  # Contador de dedos levantados

            if points_list:  # Verifica se existem pontos de referência da mão
                if points_list[4][0] < points_list[3][0]:  # Verifica se o dedo indicador está levantado
                    finger_count += 1  # Incrementa o contador de dedos
                for i in finger_ids:  # Itera sobre os índices dos pontos das pontas dos dedos
                    if points_list[i][1] < points_list[i - 2][1]:  # Verifica se o dedo está levantado
                        finger_count += 1 # Incrementa o contador de dedos

            cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)  # Desenha um retângulo azul no canto superior esquerdo
            cv2.putText(img, str(finger_count), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5) # Escreve o número de dedos levantados dentro do retângulo azul

    cv2.imshow('Imagem', img)  # Mostra o frame processado na janela chamada "Imagem"

    key = cv2.waitKey(1)  # Aguarda uma tecla ser pressionada (1 milissegundo de tempo de espera)
    if key == 81 or key == 113:  # Verifica se a tecla 'Q' ou 'q' foi pressionada para interromper o programa
        break  # Se for, sai do loop

video.release() # Libera o objeto de captura de vídeo
cv2.destroyAllWindows() # Fecha todas as janelas abertas pelo OpenCV