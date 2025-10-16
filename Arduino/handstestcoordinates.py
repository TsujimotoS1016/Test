import cv2
import mediapipe as mp
import serial

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

ser = serial.Serial('com3',9600)
ser.setDTR(False)

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
        image.flags.writeable = False

        results = hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        landmarks = results.multi_hand_landmarks
        if landmarks:
            ser.write(1)
        image = cv2.flip(image,1)
        cv2.imshow('test',image)
        if cv2.waitKey(5) & 0xFF ==27:
            break
    cap.release()
    ser.close()