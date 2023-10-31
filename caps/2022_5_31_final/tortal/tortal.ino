#include <Servo.h>
Servo myservo;
int rgtecho = A0;        //오른쪽 초음파센서
int rgttrig = A1;
int lftecho = A2;        //왼쪽 초음파센서
int lfttrig = A3;
int mtecho = A4;         //정면 초음파센서
int mttrig = A5;
int p = 41;       //서보모터 각도
float spd = 50;   //전진 모터 속도
float spd2 = 0;  //후진 모터 속도
int rasp = 0;    //라즈베리 주행
int raspr = 0;

void setup() {
  Serial.begin(9600);
  pinMode(rgttrig, OUTPUT);
  pinMode(rgtecho, INPUT);
  pinMode(lfttrig, OUTPUT);
  pinMode(lftecho, INPUT);
  pinMode(mttrig, OUTPUT);
  pinMode(mtecho, INPUT);    
  pinMode(8, OUTPUT);      //우회전 세기를 pwm 방식으로 제어
  pinMode(9, OUTPUT);      //좌회전 세기르 pwm 방식으로 제어
  pinMode(10, OUTPUT);      //HIGH 주면 좌회전 가능
  pinMode(11, OUTPUT);      //HIGH 주면 우회전 가능
  digitalWrite(10, HIGH);
  digitalWrite(11, HIGH);
  myservo.attach(12);
  myservo.write(p);

  
  analogWrite(8, spd2);
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
  
  if(Serial.available()){
    
    int raspr = Serial.read();   //라즈베리파이에서 읽어오는 값
    
    rasp = raspr - 61;
  

    if(rasp == 0) {
      rasp = p;
    }

    if(rasp != 53) {
      p = rasp;
    }
    myservo.write(p);    //라즈베리파이에서 읽어온 값을 서보모터로


  
  /*
    spd = (spd / 4) * 3;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);    //모터 속도 150rpm 
    
  if(rdist < 7){      // 오른쪽 장애물이 7cm이내로 오면 서보모터 오른쪽 이동 (각도 정면 기준 6도)
    p += 6;
    spd = spd / 3;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);      //모터 속도 90rpm  
  }
  if(ldist < 7){      // 왼쪽 장애물이 7cm이내로 오면 서보모터 왼쪽 이동   (각도 정면 기준 -6도)
    p -= 6;
    spd = spd / 3;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);   //모터 속도 90rpm    
  }
  if((ldist < 7) && (rdist < 7)){      // 양쪽이 모두 7cm 이내일 때
    if(ldist < rdist){                   // 왼쪽이 오른쪽보다 더 가까이 있으면 서보모터 왼쪽으로 이동   (각도 정면 기준 -6도)
      p -= 6;
      spd = spd / 3;
      spd2 = 0;
      myservo.write(p);
      analogWrite(8, spd2);
      analogWrite(9, spd);       //모터 속도 90rpm  
    }
    if(rdist < ldist){                  // 오른쪽이 왼쪽보다 더 가까이 있으면 서보모터 오른쪽으로 이동    (각도 정면 기준 6도)
      p += 6;
      spd = spd / 3;
      spd2 = 0;
      myservo.write(p);
      analogWrite(8, spd2);
      analogWrite(9, spd);        //모터 속도 90rpm    
    }
    if(rdist == ldist){                //7cm 이내 양쪽 거리 같으면 정면(각도 정면)
    p = 41;
    spd = spd / 2;
    spd2 = 0;
    analogWrite(8, spd2);
    analogWrite(9, spd);        //모터 속도 90rpm
  }
  
  if(dist < 7){       //정면에 7cm 이내에 장애물
    spd = 0;
    spd2 = 117;
    analogWrite(9, spd);       
    analogWrite(8, spd2);     // 후진 117rpm
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
  Serial.print("  spd2 = ");
  Serial.println(spd2);
  Serial.print("\n");

  if (rasp == 53) {
    spd = 0;
    
  }

  else {
    spd = 50;
  }
  
  spd2 = 0;

  analogWrite(8, spd2);
  analogWrite(9, spd);      //모터 속도 200rpm   
  }
  
}
