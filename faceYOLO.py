from ultralytics import YOLO
import cv2
import time

model = YOLO("best.pt")

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("カメラを開けませんでした。カメラが接続されているか確認してください。")
    exit()

# 前回の顔判断時刻を記録する変数
last_detection_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを読み込めませんでした。ストリームを終了します。")
        break

    # フレームを左右反転
    # flipCode=1 は左右反転（水平フリップ）を意味します
    flipped_frame = cv2.flip(frame, 1) 

    # 現在時刻を取得
    current_time = time.time()

    # 5秒以上経過していたら顔を判断
    # 検出は反転前のオリジナルフレームで行うか、反転後のフレームで行うか、用途によるので注意
    # 通常はプレビューだけ反転し、検出はオリジナルフレームで行います。
    # ここでは検出も反転したフレームで行う例にしています。
    if current_time - last_detection_time >= 5.0:
        results = model(flipped_frame) # 左右反転したフレームで顔の検出を実行
        
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                if cls_id == 0:
                    print("Me detected!")
                    # サーボ動作コードなどをここに追加
                else:
                    print("Not me")
        
        # 顔判断時刻を更新
        last_detection_time = current_time
    
    # 左右反転したフレームをプレビュー画面に表示
    cv2.imshow("Camera Preview (Flipped)", flipped_frame) 
    
    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()