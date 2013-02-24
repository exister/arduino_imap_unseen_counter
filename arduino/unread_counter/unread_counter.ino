#define CLOCK_PIN 2
#define RESET_PIN 3
#define SOUND_PIN 4

void resetNumber() {
  digitalWrite(RESET_PIN, HIGH);
  digitalWrite(RESET_PIN, LOW);
}

void showNumber(int value) {
  resetNumber();
  
  while (value--) {
    digitalWrite(CLOCK_PIN, HIGH);
    digitalWrite(CLOCK_PIN, LOW);
  }
}

void setup() {
  pinMode(RESET_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(SOUND_PIN, OUTPUT);
  resetNumber();
  delay(1000);
  Serial.begin(9600);
}

char inValue = 0;
int pr = 0;

void loop() {
  if (Serial.available() > 0) {
    inValue = Serial.read() - '0';
    Serial.print("I received: ");
    Serial.println(inValue, DEC);
    
    if (inValue >= 0 && inValue <= 99) {
      if (inValue != pr) {
        tone(SOUND_PIN, 262, 1000/4);
        pr = inValue;
      }
      showNumber(inValue);
    }
    else {
      Serial.println("Only numbers from 0 to 99 are supported.");
    }
  }
}
