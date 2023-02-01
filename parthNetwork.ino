#include<Servo.h>
//2, 3, 4, 5, 6, 7, 46



Servo front_right_vertical;
Servo front_left_vertical;
Servo back_right_vertical;
Servo back_left_vertical;
Servo front_right_horizontal;
Servo front_left_horizontal;
Servo back_right_horizontal;
Servo back_left_horizontal;
Servo claw;
Servo claw_rotate;
Servo camera_one;
Servo camera_two;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("RESET");
  //8, 46, 5, 7
  //3, 6, 4, 2
  front_right_vertical.attach(5); // 5
  front_left_vertical.attach(2);
  back_right_vertical.attach(6); //6 and  46
  back_left_vertical.attach(7);

  front_right_horizontal.attach(8); //8
  front_left_horizontal.attach(4); //4
  back_right_horizontal.attach(46); //46
  back_left_horizontal.attach(3);

  claw.attach(9);
  claw_rotate.attach(10);
  camera_one.attach(11);
  camera_two.attach(45);
  front_right_vertical.writeMicroseconds(1500);
  front_left_vertical.writeMicroseconds(1500);
  back_right_vertical.writeMicroseconds(1500);
  back_left_vertical.writeMicroseconds(1500);
  front_right_horizontal.writeMicroseconds(1500);
  front_left_horizontal.writeMicroseconds(1500);
  back_right_horizontal.writeMicroseconds(1500);
  back_left_horizontal.writeMicroseconds(1500);
  claw.write(1500);
  claw_rotate.write(1225);
  camera_one.write(1500);
  camera_two.write(1500);
  delay(1000);
  Serial.println("ready");
}

void loop() {
  Serial.print(Serial.available());
  while (Serial.available()) {
    String input = Serial.readStringUntil('x');
    Serial.println(input);
    int dir = input.substring(0, 1).toInt();
    int misc = input.substring(1, 2).toInt();
    int multiplier = 380;
    float val = input.substring(2, input.length() - 1).toFloat();
    int thruster_value = val * multiplier;
    //Serial.println("direction " + String(dir) + " thruster_value " + String(thruster_value));
    if (dir == 4) {
      claw.write((val * 700) + 1500);
    }
    if (dir == 5) {
      claw_rotate.write((val * 750) + 1500);

    }
    if (dir == 6) {
      camera_one.write((val * 400) + 1500);
    }
    if (dir == 7) {
      camera_two.write((val * 400) + 1500);
    }
    //sway MIGHT NEED FIX
    if (dir == 0) {
      //  Serial.println("writing values to FRH, BRH, FLH, BLH");

      front_right_vertical.writeMicroseconds(1500);
      back_right_vertical.writeMicroseconds(1500);
      front_left_vertical.writeMicroseconds(1500);
      back_left_vertical.writeMicroseconds(1500);
      front_right_horizontal.writeMicroseconds(thruster_value + 1500);
      back_right_horizontal.writeMicroseconds(thruster_value + 1500);
      front_left_horizontal.writeMicroseconds(thruster_value + 1500);
      back_left_horizontal.writeMicroseconds(thruster_value + 1500);


    }
    //surge
    else if (dir == 1) {
      front_right_vertical.writeMicroseconds(1500);
      back_right_vertical.writeMicroseconds(1500);
      front_left_vertical.writeMicroseconds(1500);
      back_left_vertical.writeMicroseconds(1500);
      front_right_horizontal.writeMicroseconds(thruster_value + 1500);
      front_left_horizontal.writeMicroseconds(-1 * thruster_value + 1500);
      back_right_horizontal.writeMicroseconds(-1 * thruster_value + 1500);
      back_left_horizontal.writeMicroseconds(thruster_value + 1500);

    }
    //heave
    else if (dir == 3) {
      front_right_horizontal.writeMicroseconds(1500);
      back_right_horizontal.writeMicroseconds(1500);
      front_left_horizontal.writeMicroseconds(1500);
      back_left_horizontal.writeMicroseconds(1500);
      front_right_vertical.writeMicroseconds(thruster_value + 1500);
      front_left_vertical.writeMicroseconds(thruster_value * -1 + 1500);
      back_right_vertical.writeMicroseconds(thruster_value * -1 + 1500);
      back_left_vertical.writeMicroseconds(thruster_value + 1500);

    }
    //yaw
    else if (dir == 2) {
      front_right_vertical.writeMicroseconds(1500);
      back_right_vertical.writeMicroseconds(1500);
      front_left_vertical.writeMicroseconds(1500);
      back_left_vertical.writeMicroseconds(1500);
      front_right_horizontal.writeMicroseconds(thruster_value + 1500);
      back_right_horizontal.writeMicroseconds(-1 * thruster_value + 1500);
      front_left_horizontal.writeMicroseconds(thruster_value + 1500);
      back_left_horizontal.writeMicroseconds(thruster_value * -1+ 1500);

    }


  }
}
