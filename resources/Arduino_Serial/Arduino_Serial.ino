//Caracteres maiúsculo desligado
char L1  = 'A';
char L2  = 'B';
char L3  = 'C';
char L4  = 'D';
char L5  = 'E';
char L6  = 'F';
char L7  = 'G';
char L8  = 'H';
char L9  = 'I';
char L10 = 'J';
char L11 = 'K';
char L12 = 'L';

void setup() {
  Serial.begin(9600); 
  pinMode(13, OUTPUT);  // a, A
  pinMode(2, OUTPUT);   // b, B
  pinMode(3, OUTPUT);   // c, C
  pinMode(4, OUTPUT);   // d, D
  pinMode(5, OUTPUT);   // e, E
  pinMode(6, OUTPUT);   // f, F
  pinMode(7, OUTPUT);   // g, G
  pinMode(8, OUTPUT);   // h, H
  pinMode(9, OUTPUT);   // i, I
  pinMode(10, OUTPUT);  // j, J
  pinMode(11, OUTPUT);  // k, K
  pinMode(12, OUTPUT);  // l, L
}

void loop() {
  if (Serial.available() > 0) {   // Verifica se há dados recebidos
    char data = Serial.read();    // Lê o dado recebido
    
    if (data == 'a') {
      digitalWrite(13, HIGH);
      L1 = 'a';
    } else if (data == 'A') {
      digitalWrite(13, LOW);
      L1 = 'A';
    }

    if (data == 'b') {
      digitalWrite(2, HIGH);
      L2 = 'b';
    } else if (data == 'B') {
      digitalWrite(2, LOW);
      L2 = 'B';
    }

    if (data == 'c') {
      digitalWrite(3, HIGH);
      L3 = 'c';
    } else if (data == 'C') {
      digitalWrite(3, LOW);
      L3 = 'C';
    }

    if (data == 'd') {
      digitalWrite(4, HIGH);
      L4 = 'd';
    } else if (data == 'D') {
      digitalWrite(4, LOW);
      L4 = 'D';
    }

    if (data == 'e') {
      digitalWrite(5, HIGH);
      L5 = 'e';
    } else if (data == 'E') {
      digitalWrite(5, LOW);
      L5 = 'E';
    }

    if (data == 'f') {
      digitalWrite(6, HIGH);
      L6 = 'f';
    } else if (data == 'F') {
      digitalWrite(6, LOW);
      L6 = 'F';
    }

    if (data == 'g') {
      digitalWrite(7, HIGH);
      L7 = 'g';
    } else if (data == 'G') {
      digitalWrite(7, LOW);
      L7 = 'G';
    }

    if (data == 'h') {
      digitalWrite(8, HIGH);
      L8 = 'h';
    } else if (data == 'H') {
      digitalWrite(8, LOW);
      L8 = 'H';
    }

    if (data == 'i') {
      digitalWrite(9, HIGH);
      L9 = 'i';
    } else if (data == 'I') {
      digitalWrite(9, LOW);
      L9 = 'I';
    }

    if (data == 'j') {
      digitalWrite(10, HIGH);
      L10 = 'j';
    } else if (data == 'J') {
      digitalWrite(10, LOW);
      L10 = 'J';
    }

    if (data == 'k') {
      digitalWrite(11, HIGH);
      L11 = 'k';
    } else if (data == 'K') {
      digitalWrite(11, LOW);
      L11 = 'K';
    }

    if (data == 'l') {
      digitalWrite(12, HIGH);
      L12 = 'l';
    } else if (data == 'L') {
      digitalWrite(12, LOW);
      L12 = 'L';
    }

    if (data == '0') {
      char estado[] = {L1,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12};
      Serial.println(estado);
    }

  }
  delay(100);
}
