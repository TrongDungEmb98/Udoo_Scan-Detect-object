
#include <Servo.h>

Servo myservo1;
Servo myservo2;

int x=90,y=90;
int data;

void setup() {
  
  myservo1.attach(9);
  myservo2.attach(10);
  myservo1.write(90);
  myservo2.write(90);  
  Serial.begin(115200);
}
void loop() {
/*  if (Serial.available())
  {
    data = Serial.read();
    //myservo1.write(data);
    //Serial.print(data);
  }*/
//read data uart...................................
  if(Serial.available())
  {  
    data = Serial.read() - 48;
    //control servo....................................
  switch (data) {
    case 1 :{
      if(x<180){
        x-=1; 
      } 
      break;
     }
     
    case 2 :{
      if(x>0){
        x+=1;
      } 
      break;
     }

     case 3 :{
      if(y<180){
        y+=1; 
      } 
      break;
     }
     
    case 4 :{
      if(y>0){
        y-=1;
      } 
      break;
     }
     case 0: 
            x=y=90;
            break;
  }
//........................
     myservo1.write(x);
     myservo2.write(y);
  }
  
}
