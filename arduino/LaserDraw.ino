#include <Servo.h>

Servo azServo;
Servo alServo;

void setup() {
  Serial.begin(38400);
    
  azServo.attach(9);
  alServo.attach(10);

  Serial.write(1);
}

void loop() {
  if (Serial.available() > 13) {
    char strBuffer[8];
    
    for (int i = 0; i < 7; i++) {
      strBuffer[i] = Serial.read();
    }
    strBuffer[7] = '\0';
    int x = String(strBuffer).toDouble();

    for (int i = 0; i < 7; i++) {
      strBuffer[i] = Serial.read();
    }
    strBuffer[7] = '\0';
    int y = String(strBuffer).toDouble();

    azServo.write(x);
    alServo.write(y);

    Serial.write(1);
  }
}