#define RELAY_PIN 7

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  Serial.begin(9600);
  lockSolenoid();  // Lock the solenoid by default
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'U') {
      unlockSolenoid();
    } 
    else if (command == 'L') {
      lockSolenoid();
    }
  }
}

// Unlock the solenoid
void unlockSolenoid() {
  digitalWrite(RELAY_PIN, HIGH);
  delay(5000);  // Keep solenoid open for 5 seconds
  lockSolenoid();
}

// Lock the solenoid
void lockSolenoid() {
  digitalWrite(RELAY_PIN, LOW);
}
