# Este código detecta apenas uma mão

# Importando as bibliotecas necessárias
import cv2
import mediapipe as mp

# Inicializando a captura de video da camera padrão (webcam)
video = cv2.VideoCapture(0)
# Inicializando o detector de mãos do mediapipe, limitando a detecção a apenas uma mão
hands = mp.solutions.hands.Hands(max_num_hands=1)
# Inicializando a ferramenta para desenhar pontos e conexões nas mãos detectadas
mpDraw = mp.solutions.drawing_utils

# Loop infinito para processar cada frame do vídeo capturado
while True:
    # Lendo o frame atual do vídeo
    success, img = video.read()
    if not success:
        break

    # Convertendo o frame de BGR para RGB
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Processando a imagem com o detector de mãos do mediapipe
    results = hands.process(imgRGB)
    # Obtendo os pontos das mãos detectadas
    handPoints = results.multi_hand_landmarks

    # Verificando se alguma mão foi detectada na imagem
    if handPoints:
        # Desenhando os pontos e conexões das mãos na imagem
        for points in handPoints:
            mpDraw.draw_landmarks(img, points, mp.solutions.hands.HAND_CONNECTIONS)
            # Obtendo a lista de coordenadas dos pontos da mão detectada
            points_list = []
            for id, cord in enumerate(points.landmark):
                h, w, _ = img.shape
                cx, cy = int(cord.x * w), int(cord.y * h)
                points_list.append((cx, cy))

            # Definindo os IDs dos pontos dos dedos da mão detectada
            finger_ids = [8, 12, 16, 20]
            finger_count = 0

            # Contando quantos dedos estão levantados
            if points_list:
                if points_list[4][0] < points_list[3][0]:
                    finger_count += 1
                for i in finger_ids:
                    if points_list[i][1] < points_list[i - 2][1]:
                        finger_count += 1

            # Desenhando um retângulo na imagem para exibir o número de dedos levantados
            cv2.rectangle(img, (80, 10), (200, 110), (255, 0, 0), -1)
            cv2.putText(img, str(finger_count), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)
            # Exibindo o número de dedos levantados no console
            print(finger_count)

    # Exibindo a imagem com as marcações de pontos e dedos
    cv2.imshow('Imagem', img)

    # Com essa função o programa só irá fechar apertando a tecla 'q'
    key = cv2.waitKey(1)
    if key==81 or key==113:
        break

# Liberando a captura de vídeo e fechando as janelas abertas
video.release()
cv2.destroyAllWindows()
