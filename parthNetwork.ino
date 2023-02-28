#include<Servo.h>

Servo front_right;
Servo front_left;
Servo back_right;
Servo back_left;
Servo vert_front;
Servo vert_back;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("RESET");
  front_right.attach();
  front_left.attach();
  back_right.attach();
  back_left.attach();
  vert_front.attach();
  vert_back.attach();
  front_right.writeMicroseconds(1500);
  front_left.writeMicroseconds(1500);
  back_right.writeMicroseconds(1500);
  back_left.writeMicroseconds(1500);
  vert_front.writeMicroseconds(1500);
  vert_back.writeMicroseconds(1500);
  delay(1000);
  Serial.println("READY");
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    String input = Serial.readStringUntil('x');
    Serial.println(input);
    float thrusters[6];
    int r=0, t=0;
    for (int i=0; i < input.length(); i++)
    { 
     if(input.charAt(i) == ',') 
      { 
        thrusters[t] = input.substring(r, i).toFloat(); 
        r=(i+1); 
        t++; 
      }
    }
    for(int i = 0;i < 6;i++){
      Serial.print(String(thrusters[i]) + " ");
    }
    front_left.writeMicroseconds(thrusters[0]);
    front_right.writeMicroseconds(thrusters[1]);
    back_left.writeMicroseconds(thrusters[2]);
    back_right.writeMicroseconds(thrusters[3]);
    vert_front.writeMicroseconds(thrusters[4]);
    vert_back.writeMicroseconds(thrusters[5]);
    Serial.println();
  }

}
