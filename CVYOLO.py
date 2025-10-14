from ultralytics import YOLO
import cv2
import time

# Haar Cascadeで軽く顔検出
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model = YOLO("best.pt")
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした。カメラが接続されているか確認してください。")
    exit()

last_boxes = []

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み込めませんでした。終了します。")
        break

    flipped_frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        print(f"顔検出: {len(faces)}個。YOLO推論を行います。")
        results = model(flipped_frame)
        last_boxes = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])

                if cls_id == 0:
                    color = (0, 255, 0)
                    print("✅ Me detected!")
                else:
                    color = (0, 0, 255)
                    print("❌ Not me")

                last_boxes.append((x1, y1, x2, y2, color))

    else:
        print("顔が画面に映っていません。YOLO推論はスキップします。")

    for x1, y1, x2, y2, color in last_boxes:
        cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), color, 2)

    cv2.imshow("Camera Preview (Flipped)", flipped_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
