String a;
#include <Servo.h>

Servo myservo; 
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  
  myservo.attach(9);
  pinMode(8, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    a= Serial.readString();// read the incoming data as string
    //Serial.println(a);
  }
  UserInterface();
}

void UserInterface(){
  digitalWrite(13, LOW);
  if (a == "lock\n"){
    myservo.write(45);
    a="";
   }
  else if (a == "unlock\n"){
    myservo.write(90);
    a="";
  }
  else if(a == "check\n"){
    if (ultrasonicDistance()< 10){
      Serial.println("Yes");
    }else{
      Serial.println("No");
    }
    a="";
  }
  else if(a == "door\n"){
    if (!digitalRead(8)){
      Serial.println("Yes");
    }else{
      Serial.println("No");
    }
    a="";
  }
  else{
      //Serial.println("Command Unknown");
  }
}

///UltrasonicDistance
const int pingPin = 7; // Trigger Pin of Ultrasonic Sensor
const int echoPin = 6; // Echo Pin of Ultrasonic Sensor
long ultrasonicDistance(){
   long duration,cm;
   pinMode(pingPin, OUTPUT);
   digitalWrite(pingPin, LOW);
   delayMicroseconds(2);
   digitalWrite(pingPin, HIGH);
   delayMicroseconds(10);
   digitalWrite(pingPin, LOW);
   pinMode(echoPin, INPUT);
   duration = pulseIn(echoPin, HIGH);
   cm = duration / 29 / 2;
   return cm;
}
