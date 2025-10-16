from ultralytics import YOLO
import cv2
import time
import gpiozero
from signal import pause
import LCD1602


# Haar cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# GPIO pin settings
BUTTON_PIN = 17
BUZZER_PIN = 23
LED_PIN = 24
servo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)

# YOLOv8
model = YOLO("best.pt")

# Devices
led = gpiozero.DigitalOutputDevice(LED_PIN)
buzzer = gpiozero.DigitalOutputDevice(BUZZER_PIN)
button = gpiozero.Button(BUTTON_PIN)

def unlock_door():
    print("Open the door")
    setup("Open the door")
    buzzer.on()
    time.sleep(1)
    buzzer.off()
    led.on()
    time.sleep(1)
    led.off()


    servo.mid()
    time.sleep(1)
    servo.min()
    time.sleep(0.5)



    
def setup(message):
    LCD1602.init(0x27, 1)
    LCD1602.write(0, 0, message)
    
def run_inference():
    print("Opening camera...")
    setup("Opening camera...")
    
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera could not be opened.")
        setup("Camera could not be opened.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("No frame captured.")
                break

            results = model(frame)

            for r in results:
                if r.boxes.cls.numel() == 0:
                    continue
                cls_id = int(r.boxes.cls[0])
                if cls_id == 0:  # "Me" detected
                    print("Me detected!")
                    setup("Me detected!")
                    unlock_door()
                    cap.release()
                    return

            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def on_button_pressed():
    print("Button was pressed.")
    setup("Button was pressed.")
    buzzer.on()
    time.sleep(2)
    buzzer.off()
    run_inference()

button.when_pressed = on_button_pressed

print("Waiting for button press...")
setup("Waiting for button press...")
pause()