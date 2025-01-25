const int relayPin = 40;
const int humiditySensor = 52;
const int analogPin = A8;

int sensorData = 0;
char stringSensorData[6];  // Increased size to handle larger strings

void setup() {
    pinMode(relayPin, OUTPUT);    // Configure relay pin as output
    digitalWrite(relayPin, HIGH);  // Ensure the relay starts OFF
    Serial.begin(9600);

    delay(2000);
}


void loop() {
  // Read analog sensor data
  sensorData = analogRead(analogPin);

  // Convert sensor data to string using built-in itoa()
  itoa(sensorData, stringSensorData, 10);

  // Send sensor data to Raspberry Pi
  Serial.print(stringSensorData);
  Serial.print('\n');  // Append newline manually


  // Delay before the next reading
  delay(1000);

  // Check if data is available from Raspberry Pi
  if (Serial.available()) {
    // Read incoming control command
    String control = Serial.readStringUntil('\n');  // Read until newline
    control.trim();  // Remove leading/trailing whitespace


    // Control relay based on received command
    if (control.equals("true")) {
      digitalWrite(relayPin, LOW);  // Turn relay ON
    } else {
      digitalWrite(relayPin, HIGH);   // Turn relay OFF
    }
  }
}
