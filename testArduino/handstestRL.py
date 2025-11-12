import cv2
import mediapipe as mp
#import serial

landmark_line_ids = [ 
    (0, 1), (1, 5), (5, 9), (9, 13), (13, 17), (17, 0),  # 掌
    (1, 2), (2, 3), (3, 4),         # 親指
    (5, 6), (6, 7), (7, 8),         # 人差し指
    (9, 10), (10, 11), (11, 12),    # 中指
    (13, 14), (14, 15), (15, 16),   # 薬指
    (17, 18), (18, 19), (19, 20),   # 小指
]


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

#ser = serial.Serial('com3',9600)
#ser.setDTR(False)

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success,image = cap.read()
        if not success:
            break
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        image = cv2.flip(image,1)
        image_h, image_w, _ = image.shape

        results = hands.process(image)
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)


        if results.multi_hand_landmarks:
            # 検出した手の数分繰り返し
            for h_id, hand_landmarks in enumerate(results.multi_hand_landmarks):

                # landmarkの繋がりをlineで表示
                for line_id in landmark_line_ids:
                    lm = hand_landmarks.landmark[line_id[0]]
                    lm_pos1 = (int(lm.x * image_w), int(lm.y * image_h))
                    # 2点目座標取得
                    lm = hand_landmarks.landmark[line_id[1]]
                    lm_pos2 = (int(lm.x * image_w), int(lm.y * image_h))
                    # line描画
                    cv2.line(image, lm_pos1, lm_pos2, (128, 0, 0), 1)

                #landmarkをcircleで表示
                z_list = [lm.z for lm in hand_landmarks.landmark]
                z_min = min(z_list)
                z_max = max(z_list)
                for lm in hand_landmarks.landmark:
                    lm_pos = (int(lm.x * image_w), int(lm.y * image_h))
                    lm_z = int((lm.z - z_min) / (z_max - z_min) * 255)
                    cv2.circle(image, lm_pos, 3, (255, lm_z, lm_z), -1)

                hand_texts = []
                for c_id, hand_class in enumerate(results.multi_handedness[h_id].classification):
                    hand_texts.append("#%d-%d" % (h_id, c_id))
                    hand_texts.append("- Label:%s" % (hand_class.label))
                    hand_texts.append("- Score:%3.2f" % (hand_class.score * 100))
                
                lm = hand_landmarks.landmark[0]
                lm_x = int(lm.x * image_w) -50
                lm_y = int(lm.y * image_h) -10
                lm_c = (64, 0, 0)
                font = cv2.FONT_HERSHEY_SIMPLEX

                for cnt, text in enumerate(hand_texts):
                    cv2.putText(image, text, (lm_x, lm_y + 10 * cnt), font, 0.3, lm_c, 1)

        
           #ser.write(landmarks)
        print(lm_x)
        #image = cv2.flip(image,1)
        cv2.imshow('test',image)
        if cv2.waitKey(5) & 0xFF ==27:
            break
    cap.release()
    #ser.close()