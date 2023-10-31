#include <Servo.h>
#include <SoftwareSerial.h>
Servo myservo;
int rgtecho = A0;        //오른쪽 초음파센서
int rgttrig = A1;
int lftecho = A2;        //왼쪽 초음파센서
int lfttrig = A3;
int mtecho = A4;         //정면 초음파센서
int mttrig = A5;
int p = 41;       //서보모터 각도
float spd = 50;   //전진 모터 속도
float strling = 1;  //후진 모터 속도
int rasp = 0;    //라즈베리 주행
int raspr = 0;
int z = 103; //servo +=
int pass = 0;

int delay_count = 0;

void setup() {
  Serial.begin(9600);
  //Serial1.begin(9600);
  pinMode(rgttrig, OUTPUT);
  pinMode(rgtecho, INPUT);
  pinMode(lfttrig, OUTPUT);
  pinMode(lftecho, INPUT);
  pinMode(mttrig, OUTPUT);
  pinMode(mtecho, INPUT);    
  pinMode(8, OUTPUT);      //우회전 세기를 pwm 방식으로 제어
  pinMode(9, OUTPUT);      //좌회전 세기르 pwm 방식으로 제어
  myservo.attach(12);
  myservo.write(p);

  
  digitalWrite(8, strling);
  analogWrite(9, spd);      //모터 속도 200rpm   
  
}



void loop() {
  /*digitalWrite(rgttrig, HIGH);                   //오른쪽 초음파센서 거리
  delayMicroseconds(10);
  digitalWrite(rgttrig, LOW);
  int rdist = pulseIn(rgtecho, HIGH)*17/1000;
  digitalWrite(lfttrig, HIGH);                  //왼쪽 초음파센서
  delayMicroseconds(10);
  digitalWrite(lfttrig, LOW);
  int ldist = pulseIn(lftecho, HIGH)*17/1000;
  digitalWrite(mttrig, HIGH);                   //정면 초음파센서
  delayMicroseconds(10);
  digitalWrite(mttrig, LOW);
  int dist = pulseIn(mtecho, HIGH)*17/1000;*/
  
/*
  if(Serial1.available()) {
  myservo.write(p);
    while(1){
      if(Serial1.available()){
      Serial.write(Serial1.read());
      switch (Serial1.read()) {
       case 'w':          //정면
         p = 41;
         myservo.write(p);
         break;

       case 'a':         //우회전
         p = 35;      
         myservo.write(p);
         break;

       case 'd':         //좌회전
         p = 47;      
         myservo.write(p);
         break;

       case 'h':                       // (세모) 모터 속도 160rpm
         spd = 160;
         strling = LOW;
         digitalWrite(8, strling);
         analogWrite(9, spd);
         Serial.println(spd);
         break;

       case 'l':                   // (원) 후진 모터 속도 117rpm
         spd = 117;
         strling = HIGH;
         digitalWrite(8, strling);
         analogWrite(9, spd);
         Serial.println(strling);
         break;

       case 'j':                  //(네모) 모터 정지
         spd = 0;
         strling = 0;
         Serial.print(spd);
         Serial.println(strling);
         break;
         
       case 'c':
       goto exit;
       break;
      }
    }
    }
  }

  exit:
  */
  
  if(Serial.available()){

    
    int raspr = Serial.read();   //라즈베리파이에서 읽어오는 값


    if(raspr >= 91 and raspr <= 96 and delay_count == 0) {
      delay(2000); 
      delay_count = 1;
    }

    else if(raspr >= 100 and raspr <= 106 and delay_count != 0) {
      delay_count = 0;
    }

    else if(raspr <= 111 and raspr >= 109 and delay_count == 0) {
      delay(2000);
      delay_count = -1;
    }
    
    //rasp = raspr - 64;
    rasp = raspr - 64;
    

    if(rasp == 0) {
      rasp = p;
    }

    if(rasp != 50 and rasp != 55) {
      p = rasp;
    }

    else {
      p = z;
    }   


    
    if(rasp == 55){ //blue
      pass = 1;
      spd == 0;
      delay(2000);
      spd = 50;
      delay(3000);
      /*
      while(1){
        delay(500);
        if(Serial.read
      }
      */
    }
     if(rasp == 50){ //red
      pass = 1;
      spd == 0;
      delay(2000);
      spd = 50;
      delay(3000);
     }

     if(rasp > z){    //servo+=
     p+=6;
     }
     if(pass == 0){
      myservo.write(p);    //라즈베리파이에서 읽어온 값을 서보모터로
     }
    

    z = rasp;
  
  /*
    spd = (spd / 4) * 3;
    strling = HIGH;
    myservo.write(p);
    digitalWrite(8, strling);
    analogWrite(9, spd);    //모터 속도 150rpm 
    
  if(rdist < 7){      // 오른쪽 장애물이 7cm이내로 오면 서보모터 오른쪽 이동 (각도 정면 기준 6도)
    p += 6;
    spd = spd / 3;
    strling = LOW;
    myservo.write(p);
    digitalWrite(8, strling);
    analogWrite(9, spd);      //모터 속도 90rpm  
  }
  if(ldist < 7){      // 왼쪽 장애물이 7cm이내로 오면 서보모터 왼쪽 이동   (각도 정면 기준 -6도)
    p -= 6;
    spd = spd / 3;
    spd2 = 0;
    myservo.write(p);
    digitalWrite(8, strling);
    analogWrite(9, spd);   //모터 속도 90rpm    
  }
  if((ldist < 7) && (rdist < 7)){      // 양쪽이 모두 7cm 이내일 때
    if(ldist < rdist){                   // 왼쪽이 오른쪽보다 더 가까이 있으면 서보모터 왼쪽으로 이동   (각도 정면 기준 -6도)
      p -= 6;
      spd = spd / 3;
      spd2 = 0;
      myservo.write(p);
      digitalWrite(8, strling);
      analogWrite(9, spd);       //모터 속도 90rpm  
    }
    if(rdist < ldist){                  // 오른쪽이 왼쪽보다 더 가까이 있으면 서보모터 오른쪽으로 이동    (각도 정면 기준 6도)
      p += 6;
      spd = spd / 3;
      spd2 = 0;
      myservo.write(p);
      digitalWrite(8, strling);
      analogWrite(9, spd);        //모터 속도 90rpm    
    }
    if(rdist == ldist){                //7cm 이내 양쪽 거리 같으면 정면(각도 정면)
    p = 41;
    spd = spd / 2;
    strling = 0;
    digitalWrite(8, strling);
    analogWrite(9, spd);        //모터 속도 90rpm
  }
  
  if(dist < 7){       //정면에 7cm 이내에 장애물
    spd = 0;
    spd2 = HIGH;
    analogWrite(9, spd);       
    digitalWrite(8, strling);     // 후진 117rpm
  }
  
  Serial.print("left = ");      //시리얼모니터에 보이게 함
  Serial.print(ldist);
  Serial.print("  right = ");
  Serial.println(rdist);*/
  Serial.print("angle = ");
  Serial.println(p); 
  //Serial.print("dist = ");
  //Serial.println(dist);
  Serial.print("spd = ");
  Serial.print(spd);
  Serial.print("  strling = ");
  Serial.println(strling);
  Serial.print("\n");

  if (rasp == 53) {
    spd = 0;
    
  }

  else {
    spd = 50;
  }
  digitalWrite(8, strling);
  analogWrite(9, spd);      //모터 속도 200rpm   
  }
  pass = 0;
}
