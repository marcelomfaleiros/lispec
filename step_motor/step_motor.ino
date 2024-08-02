int p, k, wls;

void pin_high(int);

void setup() 
{ 
  Serial.begin(9600);  
  pinMode(2, OUTPUT);    // Configura os pinos d2,  
  pinMode(3, OUTPUT);    // d3, 
  pinMode(4, OUTPUT);    // d4 e 
  pinMode(5, OUTPUT);    // d5 -> saídas
  pinMode(6, INPUT);     // d6 -> saída = clockwise  
  pinMode(7, INPUT);     // d7, 
  pinMode(8, INPUT);     // d8  
  pinMode(9, INPUT);     // d9 
  pinMode(10, INPUT);    // d10 e 
  pinMode(11, INPUT);    // d11 como entradas
}

void loop() 
{         
  /*if (digitalRead(8) == LOW)
  {
    p = 5;
    while (digitalRead(8) == LOW)
    {
      pin_high(p);
      delay(5);
      p--;
      if (p < 2)
        p = 5;
    }
  }    
  if (digitalRead(9) == LOW)
  {
    p = 2;
    while (digitalRead(9) == LOW)
    {
      pin_high(p);
      delay(5);
      p++;
      if (p > 5)
        p = 2;
    }
  }    
  if (digitalRead(10) == LOW)
  {
    p = 5;
    while (digitalRead(10) == LOW)
    {
      pin_high(p);
      delay(60);
      p--;
      if (p < 2)
        p = 5;
    }
  }    
  if (digitalRead(11) == LOW)
  {
    p = 2;
    while (digitalRead(11) == LOW)
    {
      pin_high(p);
      delay(60);
      p++;
      if (p > 5)
        p = 2;
    }
  }   */ 
  if (Serial.available() > 0)   //verifica a porta serial 
  { 
    wls = Serial.parseInt();   //recebe um valor via serial em number of steps        
    if (wls > 0)    
    {           
      p = 5;
      for (k = 0; k < wls; k++) //wls = number of steps
      {
        if (digitalRead(7) == HIGH)
          break;
        pin_high(p);
        delay(6);
        p--;
        if (p < 2)
          p = 5;
      }   
    }               
    else if (wls < 0)
    {               
      p = 2;
      for (k = 0; k < (abs(wls) + 500); k++)
      {  
        if (digitalRead(6) == HIGH)
          break;
        pin_high(p);
        delay(6);
        p++;
        if (p > 5)
          p = 2;
      }
      p = 5;
      for (k = 0; k < 500; k++) 
      {  
        if (digitalRead(6) == HIGH)
          break;
        pin_high(p);
        delay(6);
        p--;
        if (p < 2)
          p = 5;
      }
    }  
    else if (wls = 0)
      pin_high(0);  
   }
}    

void pin_high(int i)
{
  switch (i)
  {
    case 0:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW
      break;
    case 2:
      digitalWrite(2, HIGH);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW 
      break;
    case 3:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, HIGH);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW 
      break;
    case 4:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, HIGH);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW 
      break;
    case 5:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, HIGH);     // Configura o pino 5 como LOW
      break;
  }
}