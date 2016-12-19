
char val = 'a'; // variable to store the data from the serial port
int found = 0;

void setup() {
Serial.begin(9600); // connect to the serial port
}

void loop () {
// read the serial port
  if(Serial.available() > 0) {
    val = Serial.read();
    found = 1;
    delay(10);
  }
  else if(Serial.available() == 0 && found == 1) {
    Serial.print("Tag\n");
    found = 0;
  }
}

