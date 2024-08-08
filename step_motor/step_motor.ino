int k, steps;

int p = 1;

void step(int);

void setup()             // pin config
{ 
  Serial.begin(9600);  
  pinMode(2, OUTPUT);    // motor control  
  pinMode(3, OUTPUT);    // motor control 
  pinMode(4, OUTPUT);    // motor control
  pinMode(5, OUTPUT);    // motor control
  pinMode(6, INPUT);     // limit switch  
  pinMode(7, INPUT);     // limit switch 
  pinMode(8, INPUT);     // remote control  
  pinMode(9, INPUT);     // remote control 
  pinMode(10, INPUT);    // remote control 
  pinMode(11, INPUT);    // remote control
  step(0);
}

void loop() 
{         
  if (digitalRead(8) == LOW)      //button pressed
  {
    step(p);
    delay(5);
    p--;
    if (p < 1)
      p = 8;
  }    
  if (digitalRead(9) == LOW)
  {
    step(p);
    delay(5);
    p++;
    if (p > 8)
      p = 1;
  }    
  if (digitalRead(10) == LOW)
  {
    step(p);
    delay(60);
    p--;
    if (p < 1)
      p = 8;
  }    
  /*if (digitalRead(11) == LOW)
  {
    step(p);
    delay(60);
    p++;
    if (p > 5)
      p = 2;
  } */ 
  if (Serial.available() > 0)   //verifica a porta serial 
  { 
    steps = Serial.parseInt();   //recebe um valor via serial em number of steps        
    if (steps > 0)    
    {           
      for (k = 0; k < steps; k++) //wls = number of steps
      {
        if (digitalRead(7) == HIGH) // if limit switch not pressed
          break;
        step(p);
        delay(4);
        p--;
        if (p < 1)
          p = 8;
      }   
    }               
    else if (steps < 0)
    {               
      for (k = 0; k < (abs(steps) + 1000); k++)
      {  
        if (digitalRead(6) == HIGH)  // if limit switch not pressed
          break;
        step(p);
        delay(4);
        p++;
        if (p > 8)
          p = 1;
      }
      for (k = 0; k < 1000; k++) 
      {  
        if (digitalRead(6) == HIGH)  // if limit switch not pressed
          break;
        step(p);
        delay(4);
        p--;
        if (p < 1)
          p = 8;
      }
    }  
    else if (steps = 0)
      step(0);  
   }
}    

void step(int i)
{
  switch (i)
  {
    case 0:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW
      break;
    case 1:
      digitalWrite(2, HIGH);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW 
      break;
    case 2:
      digitalWrite(2, HIGH);    // Configura o pino 2 como HIGH              
      digitalWrite(3, HIGH);     // Configura o pino 3 como LOW  
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
      digitalWrite(3, HIGH);     // Configura o pino 3 como LOW  
      digitalWrite(4, HIGH);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW
      break;
    case 5:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, HIGH);     // Configura o pino 4 como LOW                
      digitalWrite(5, LOW);     // Configura o pino 5 como LOW 
      break;
    case 6:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, HIGH);     // Configura o pino 4 como LOW                
      digitalWrite(5, HIGH);     // Configura o pino 5 como LOW 
      break;
    case 7:
      digitalWrite(2, LOW);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, HIGH);     // Configura o pino 5 como LOW 
      break;
    case 8:
      digitalWrite(2, HIGH);    // Configura o pino 2 como HIGH              
      digitalWrite(3, LOW);     // Configura o pino 3 como LOW  
      digitalWrite(4, LOW);     // Configura o pino 4 como LOW                
      digitalWrite(5, HIGH);     // Configura o pino 5 como LOW
      break;
  }
}