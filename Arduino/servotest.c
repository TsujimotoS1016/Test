#include <Servo.h>

Servo servo1;
Servo servo2;

void setup() {
  servo1.attach(9);  // サーボ1を9番ピンに
  servo2.attach(10); // サーボ2を10番ピンに
}

void loop() {
  // A0ピンから可変抵抗の値を読み取る (0〜1023)
  int potValue = analogRead(A0);
  
  // 読み取った値をサーボの角度 (0〜180) に変換
  int angle = map(potValue, 0, 1023, 0, 180);
  
  // 2つのサーボに同じ角度を指示
  servo1.write(angle);
  servo2.write(angle);
  
  delay(15); // サーボが動くのを少し待つ
}