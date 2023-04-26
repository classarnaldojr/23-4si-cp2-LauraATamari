import cv2
import mediapipe as mp

#usando mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#logica para identificar se pedra, papel e tesoura da mão esquerda
def getHandMoveLeft(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if (landmarks[5].x > landmarks[8].x) and (landmarks[9].x > landmarks[12].x) and (landmarks[13].x > landmarks[16].x) and (landmarks[17].x > landmarks[20].x): return "pedra"
    elif (landmarks[5].x < landmarks[8].x) and (landmarks[9].x < landmarks[12].x) and (landmarks[13].x < landmarks[16].x) and (landmarks[17].x < landmarks[20].x): return "papel"
    else: return "tesoura"
#logica para identificar se pedra, papel e tesoura da mão direita
def getHandMoveRight(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if (landmarks[5].x < landmarks[8].x) and (landmarks[9].x < landmarks[12].x) and (landmarks[13].x < landmarks[16].x) and (landmarks[17].x < landmarks[20].x): return "pedra"
    elif (landmarks[5].x > landmarks[8].x) and (landmarks[9].x > landmarks[12].x) and (landmarks[13].x > landmarks[16].x) and (landmarks[17].x > landmarks[20].x): return "papel"
    else: return "tesoura"

#iniciando em 0/nada escrito
gameText = ""
left_score = 0
right_score = 0
time = 0

#captura do video
cap = cv2.VideoCapture('pedra-papel-tesoura.mp4')

#configuracoes para identificar as maos
with mp_hands.Hands(
    model_complexity=0, 
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5) as hands:

    while True:
        success, img = cap.read()
        #revertendo imagem em BGR para identificar melhor
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #resultado do mediapipe 
        results = hands.process(img)
        #revertendo imagem para cor normal/RGB
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #desenhando os pontos nas mãos
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
            p2_move = getHandMoveRight(hls[0])
            #pegar o gesto da mao da esquerda
            p1_move = getHandMoveLeft(hls[1])
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
            #condições para add pontuação
            time = (time + 1 ) % 180
            time += 1
            if time >= 170 and time <= 170.5:
                if gameText == "Jogador 1 vence":
                    left_score += 1
                elif gameText == "Jogador 2 vence":
                    right_score += 1
                else:
                    left_score == left_score
                    right_score == right_score


        #add textos
        cv2.putText(img, gameText, (600, 950), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str("Jogador 1"), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, p1_move, (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str(left_score), (100, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str('Jogador 2'), (1400, 200), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, p2_move, (1400, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)
        cv2.putText(img, str(right_score), (1400, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0), 2)

        cv2.imshow('Hands', img)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        #exibindo pontuação, e quem ganha no final
        print("PONTUACAO")
        print("Jogador 1: ", left_score, " pontos")
        print("Jogador 2: ", right_score, " pontos")
        if left_score < right_score:
            print("Jogador 2 vence")
        else:
            print("Jogador 1 vence")

cap.release()
cv2.destroyAllWindows()


