#define PIN_LASER 8
#define STEP_PIN 6
#define DIR_PIN  7

int NumSteps = 0; // global so it persists between loop() iterations

void setup() {
  Serial.begin(9600);
  pinMode(PIN_LASER, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);
  pinMode(DIR_PIN, OUTPUT);
  digitalWrite(DIR_PIN, HIGH);
}

void stepMotor(int steps, bool forward) {
  digitalWrite(DIR_PIN, forward ? HIGH : LOW);
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP_PIN, HIGH);
    delayMicroseconds(1000);
    digitalWrite(STEP_PIN, LOW);
    delayMicroseconds(1000);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "LASER_ON") {
      digitalWrite(PIN_LASER, HIGH);
      Serial.println("LASER_ON OK");

    } else if (command == "LASER_OFF") {
      digitalWrite(PIN_LASER, LOW);
      Serial.println("LASER_OFF OK");

    } else if (command == "STEP") {
      stepMotor(200, true); // 1 revolution forward
      NumSteps++;
      Serial.println("STEP OK");

    } else if (command == "RESET") {
      for (int k = 0; k < NumSteps; k++) {
        stepMotor(200, false); // 1 revolution backward per step taken
      }
      NumSteps = 0;
      Serial.println("RESET OK");

    } else {
      Serial.println("ERROR");
    }
  }
}
