from ultralytics import YOLO
import cv2
import time

model = YOLO("best.pt")

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした。カメラが接続されているか確認してください。")
    exit()

last_detection_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み込めませんでした。ストリームを終了します。")
        break

    flipped_frame = cv2.flip(frame, 1)
    current_time = time.time()

    if current_time - last_detection_time >= 5.0:
        results = model(flipped_frame)

        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])  # 信頼度を取得（0.0〜1.0）

                # クラスごとにラベルと色を設定
                if cls_id == 0:
                    label = f"Me ({conf:.2f})"
                    color = (0, 255, 0)  # 緑
                    print("Me detected! Unlocking door...")
                else:
                    label = f"Others ({conf:.2f})"
                    color = (0, 0, 255)  # 赤
                    print("Not me")

                # バウンディングボックスとラベルを描画
                cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(flipped_frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        last_detection_time = current_time

    cv2.imshow("Camera Preview (Flipped)", flipped_frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
