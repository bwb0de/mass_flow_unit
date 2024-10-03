uint8_t SensorStep = 0;

void setup() {
  Serial.begin(9600); 
  pinMode(2, OUTPUT);   
  pinMode(3, OUTPUT);   
  pinMode(4, OUTPUT);   
  pinMode(5, OUTPUT);   
  pinMode(6, OUTPUT);   
  pinMode(7, OUTPUT);   
  pinMode(8, OUTPUT);   
  pinMode(9, OUTPUT);   
  pinMode(10, OUTPUT);  
  pinMode(11, OUTPUT);  
  pinMode(12, OUTPUT);  
  pinMode(13, OUTPUT);  
}

void loop() {
  if (Serial.available() > 0) {   // Verifica se há dados recebidos
    char data = Serial.read();
    if (data == 'p') {
      SensorStep += 1;
    } else if (data == 'r') {
      SensorStep = 0;
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
    }

    if ( SensorStep > 11 ) {
      SensorStep = 1;
    }

    if ( SensorStep == 1 ) {
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('1');
    }

    else if ( SensorStep == 2 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('2');
    }

    else if ( SensorStep == 3 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('3');
    }

    else if ( SensorStep == 4 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, HIGH);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('4');
    }

    else if ( SensorStep == 5 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, HIGH);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('5');
    }

    else if ( SensorStep == 6 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, HIGH);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('6');
    }

    else if ( SensorStep == 7 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, HIGH);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('7');
    }

    else if ( SensorStep == 8 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, HIGH);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('8');
    }

    else if ( SensorStep == 9 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, HIGH);
      digitalWrite(11, LOW);
      digitalWrite(12, LOW);
      Serial.println('9');
    }

    else if ( SensorStep == 10 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, HIGH);
      digitalWrite(12, LOW);
      Serial.println('A'); //10
    }

    else if ( SensorStep == 11 ) {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      digitalWrite(6, LOW);
      digitalWrite(7, LOW);
      digitalWrite(8, LOW);
      digitalWrite(9, LOW);
      digitalWrite(10, LOW);
      digitalWrite(11, LOW);
      digitalWrite(12, HIGH);
      Serial.println('B'); //11
    }

  }
  delay(100);
}
