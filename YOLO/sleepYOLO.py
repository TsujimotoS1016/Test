from ultralytics import YOLO
import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model = YOLO("best.pt")
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした。")
    exit()

last_boxes = []
last_confidences = {}
face_absent_start = None
face_absent_threshold = 10  # 顔が消えたと判定する秒数
last_inference_time = 0     # 前回のYOLO推論時刻

def display_boxes(frame, boxes):
    for x1, y1, x2, y2, color, label, conf in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み込めませんでした。終了します。")
        break

    flipped_frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    current_time = time.time()

    if len(faces) > 0:
        face_absent_start = None  # 顔あり復帰

        if current_time - last_inference_time >= 5.0:  # 1秒ごとにYOLO推論
            results = model(flipped_frame)
            boxes_to_display = []
            current_confidences = {}

            for r in results:
                for box in r.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = "Me" if cls_id == 0 else "Other"
                    color = (0, 255, 0) if cls_id == 0 else (0, 0, 255)

                    prev_conf = last_confidences.get((x1, y1, x2, y2), 0)
                    if abs(conf - prev_conf) > 0.01:
                        print(f"{label} の信頼度が変化: {prev_conf:.2f} → {conf:.2f}")

                    current_confidences[(x1, y1, x2, y2)] = conf
                    boxes_to_display.append((x1, y1, x2, y2, color, label, conf))

            last_confidences = current_confidences
            last_boxes = boxes_to_display
            last_inference_time = current_time

    else:
        if face_absent_start is None:
            face_absent_start = current_time
            print("顔が画面に映っていません。動作を一時停止します。")
        else:
            elapsed = current_time - face_absent_start
            if elapsed > face_absent_threshold:
                print(f"{face_absent_threshold}秒間顔なし。さらにスリープ中...")

        last_boxes = []
        time.sleep(1)  # 顔がいないときは1秒待機

    display_boxes(flipped_frame, last_boxes)
    cv2.imshow("Camera Preview (Flipped)", flipped_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
