int p, k, wls;

void pin_high(int);

void setup() 
{ 
  Serial.begin(9600);  
  pinMode(2, OUTPUT);    // Digital control pin  
  pinMode(3, OUTPUT);    // Digital control pin 
  pinMode(4, OUTPUT);    // Digital control pin
  pinMode(5, OUTPUT);    // Digital control pin
  pinMode(6, INPUT);     // Limit switch  
  pinMode(7, INPUT);     // Limit switch 
  pinMode(8, INPUT);     // Remote control - up fast 
  pinMode(9, INPUT);     // Remote control - up slow
  pinMode(10, INPUT);    // Remote control - down fast 
  pinMode(11, INPUT);    // Remote control - down slow

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
        if (digitalRead(7) == HIGH) // if limit switch not pressed
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
        if (digitalRead(6) == HIGH)  // if limit switch not pressed
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