import cv2
import mediapipe as mp
import time
import uuid
import hmac
import hashlib
import base64
import requests

# --- SwitchBot API 情報 ---
TOKEN = 'eff6b9db75af19556d695435d94c3384f1a0548263fbb67ce717209cfaabf141d417b2b4b542e4dd0d8e85339a2b4ee8'
SECRET = 'a31ca16a806b0112a2e52ee3491d5276'
DEVICE_ID = '02-202404141055-53447619'

def send_switchbot_command(command: str):
    nonce = str(uuid.uuid4())
    t = str(int(round(time.time() * 1000)))
    string_to_sign = (TOKEN + t + nonce).encode('utf-8')
    secret_bytes = SECRET.encode('utf-8')
    sign = base64.b64encode(hmac.new(secret_bytes, string_to_sign, hashlib.sha256).digest()).decode('utf-8')

    headers = {
        'Authorization': TOKEN,
        't': t,
        'sign': sign,
        'nonce': nonce,
        'Content-Type': 'application/json; charset=utf8'
    }

    url = f'https://api.switch-bot.com/v1.1/devices/{DEVICE_ID}/commands'
    payload = {
        "command": command,
        "parameter": "default",
        "commandType": "command"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(f"SwitchBot response: {response.status_code}, {response.json()}")

# --- MediaPipe Hand Tracking 設定 ---
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]

cap = cv2.VideoCapture(0)
cooldown = 10  # 再検出までのクールダウン（秒）
last_trigger_time = 0

with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        image = cv2.flip(image, 1)
        image.flags.writeable = False
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        image.flags.writeable = True
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        gesture_text = ""

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                open_fingers = 0
                for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
                        open_fingers += 1

                if open_fingers == 0:
                    gesture_text = "グー"

                    # クールダウン処理（3秒間は連続送信しない）
                    current_time = time.time()
                    if current_time - last_trigger_time > cooldown:
                        print("グーを検出しました。電気を消します。")
                        send_switchbot_command("turnOff")
                        last_trigger_time = current_time

                elif open_fingers == 4:
                    gesture_text = "パー"
                    current_time = time.time()
                    if current_time - last_trigger_time > cooldown:
                        print("パーを検出しました。電気をつけます。")
                        send_switchbot_command("turnOn")
                        last_trigger_time = current_time

                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if gesture_text:
            cv2.putText(image, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        cv2.imshow('Hand Gesture + SwitchBot', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
