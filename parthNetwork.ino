void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("RESET");
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
    Serial.println();
  }

}
