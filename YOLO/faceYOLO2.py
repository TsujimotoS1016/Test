from ultralytics import YOLO
import cv2
import time

model = YOLO("best.pt")
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした。カメラが接続されているか確認してください。")
    exit()

last_detection_time = 0
last_boxes = []  # (x1, y1, x2, y2, color, confidence) のリスト

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み込めませんでした。ストリームを終了します。")
        break

    flipped_frame = cv2.flip(frame, 1)
    current_time = time.time()

    # 5秒ごとに検出
    if current_time - last_detection_time >= 5.0:
        results = model(flipped_frame)
        last_boxes = []

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])  # 信頼度 (0.0〜1.0)

                if cls_id == 0 and conf >= 0.95:
                    color = (0, 255, 0)  # 緑：自分
                    print(f"Me detected! ({conf:.2f})")
                else:
                    color = (0, 0, 255)  # 赤：他人
                    print(f"Not me ({conf:.2f})")

                # 座標、色、信頼度を保存
                last_boxes.append((x1, y1, x2, y2, color, conf))

        last_detection_time = current_time

    # 前回の検出結果を表示（枠＋信頼度）
    for x1, y1, x2, y2, color, conf in last_boxes:
        cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), color, 2)
        label = f"{conf:.2f}"
        cv2.putText(flipped_frame, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    cv2.imshow("Camera Preview (Flipped)", flipped_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
