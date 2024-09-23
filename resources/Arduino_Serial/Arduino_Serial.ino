// Código Arduino para comunicação serial
void setup() {
  Serial.begin(9600);  // Inicia a comunicação serial na velocidade 9600 baud
  pinMode(LED_BUILTIN, OUTPUT);  // Define o LED como saída
}

void loop() {
  if (Serial.available() > 0) {   // Verifica se há dados recebidos
    char data = Serial.read();    // Lê o dado recebido
    if (data == '1') {
      digitalWrite(LED_BUILTIN, HIGH);  // Liga o LED se receber '1'
      Serial.println('1');
    } else if (data == '0') {
      digitalWrite(LED_BUILTIN, LOW);   // Desliga o LED se receber '0'
      Serial.println('2');
    } else {
      Serial.println('9');
    }
  }
  delay(100);
}
