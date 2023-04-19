import cv2
import mediapipe as mp
import numpy as np
import imutils

#usando mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#logica para identificar se pedra, papel e tesoura
def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if (landmarks[5].y < landmarks[8].y) and (landmarks[9].y < landmarks[12].y) and (landmarks[13].y < landmarks[16].y) and (landmarks[17].y < landmarks[20].y): return "pedra"
    elif (landmarks[5].y > landmarks[8].y) and (landmarks[9].y > landmarks[12].y) and (landmarks[13].y > landmarks[16].y) and (landmarks[17].y > landmarks[20].y): return "papel"
    else: return "tesoura"

#captura do video
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

#gameText, string que vai mostrar quem venceu
gameText = ""

#configuracoes para identificar as maos
with mp_hands.Hands(
    model_complexity=0, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5) as hands:

    scores = [0, 0]

    while True:
        success, img = cap.read()

        #achar altura e largura do video
        h, w, _ = img.shape

        #dividir a imagem do video em 2
        half = w//2

        #separa o lado esquerdo do video
        left_part = img[:, :half]
        #separa o lado direito do video
        right_part = img[:, half:]

        #parte esquerda girando em 90 graus 
        left_up = imutils.rotate(left_part, angle=90)
        #parte direita girando em 270 graus 
        right_up = imutils.rotate(right_part, angle=270)

        #juntando os lados
        img = cv2.hconcat([left_up, right_up])

        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img)

        #identificando as maos e desenhando os pontos
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

        hls = results.multi_hand_landmarks
        #se dentro dos resuldados tiver 2 maos
        if hls and len(hls) == 2:
            #pegar o gesto da mao da direita
            p2_move = getHandMove(hls[0])
            #pegar o gesto da mao da esquerda
            p1_move = getHandMove(hls[1])
            #condicoes para quem ganha
            if success:
                if p1_move == p2_move: gameText = "Empate"
                elif p1_move == "papel" and p2_move == "pedra": 
                    gameText = "Jogador 1 vence"
                elif p1_move == "papel" and p2_move == "tesoura": 
                    gameText = "Jogador 2 vence"
                elif p1_move == "pedra" and p2_move == "tesoura": 
                    gameText = "Jogador 1 vence"
                elif p1_move == "pedra" and p2_move == "papel": 
                    gameText = "Jogador 2 vence"
                elif p1_move == "tesoura" and p2_move == "papel": 
                    gameText = "Jogador 1 vence"
                elif p1_move == "tesoura" and p2_move == "pedra": 
                    gameText = "Jogador 2 vence"
                else:
                    print("Not identified")
            else:
                success = False

            if gameText == "Jogador 1 vence":
                scores[0] += 1
            else:
                scores[1] += 1

        #voltando o video para a posicao original
        #separa o lado esquerdo do video
        left_part = img[:, :half]
        #separa o lado direito do video
        right_part = img[:, half:]

        #parte esquerda girando em 270 graus 
        left_up = imutils.rotate(left_part, angle=270)
        #parte esquerda girando em 90 graus 
        right_up = imutils.rotate(right_part, angle=90)
        
        #juntando os lados
        img = cv2.hconcat([left_up, right_up])

        #add textos
        cv2.putText(img, gameText, (600, 950), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str("Jogador 1"), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, p1_move, (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str(scores[0]), (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str('Jogador 2'), (1400, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, p2_move, (1400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str(scores[1]), (1400, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)

        cv2.imshow('Hands', img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

