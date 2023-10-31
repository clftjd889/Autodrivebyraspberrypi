#include <Servo.h>
Servo myservo;
int rgtecho = A2;        //오른쪽 초음파센서
int rgttrig = A3;
int lftecho = A4;        //왼쪽 초음파센서
int lfttrig = A5;
int mtecho = A6;         //정면 초음파센서
int mttrig = A7;
int p = 41;       //서보모터 각도
float spd = 0;   //전진 모터 속도
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
}

void loop() {
  digitalWrite(rgttrig, HIGH);                   //오른쪽 초음파센서 거리
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
  int dist = pulseIn(mtecho, HIGH)*17/1000;
  
  while(Serial.available() > 0){
    int raspr = Serial.read();                    //라즈베리파이에서 읽어오는 값
  }
  rasp = raspr - 61;
  p = rasp;
  myservo.write(p);                             //라즈베리파이에서 읽어온 값을 서보모터로
  /*
  if(rdist < 7){      // 오른쪽 장애물이 7cm이내로 오면 서보모터 오른쪽 이동 (각도 정면 기준 6도)
    p += 6;
    spd = 90;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);      //모터 속도 90rpm  
  }
  if(ldist < 7){      // 왼쪽 장애물이 7cm이내로 오면 서보모터 왼쪽 이동   (각도 정면 기준 -6도)
    p -= 6;
    spd = 90;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);   //모터 속도 90rpm    
  }
  if((ldist < 7) && (rdist < 7)){      // 양쪽이 모두 7cm 이내일 때
    if(ldist < rdist){                   // 왼쪽이 오른쪽보다 더 가까이 있으면 서보모터 왼쪽으로 이동   (각도 정면 기준 -5도)
      p -= 6;
      spd = 90;
      spd2 = 0;
      myservo.write(p);
      analogWrite(8, spd2);
      analogWrite(9, spd);       //모터 속도 90rpm  
    }
    if(rdist < ldist){                  // 오른쪽이 왼쪽보다 더 가까이 있으면 서보모터 오른쪽으로 이동    (각도 정면 기준 5도)
      p += 6;
      spd = 90;
      spd2 = 0;
      myservo.write(p);
      analogWrite(8, spd2);
      analogWrite(9, spd);        //모터 속도 90rpm    
    }
  }
  if(((ldist >= 7) && (rdist >= 7)) || (ldist == rdist)){           // 장애물이 양쪽 7cm 이상 있거나 양쪽 거리 같으면 앞만보고 이동
    p = 41;
    spd = 150;
    spd2 = 0;
    myservo.write(p);
    analogWrite(8, spd2);
    analogWrite(9, spd);    //모터 속도 150rpm 
  }
  if(dist < 7){       //정면에 7cm 이내에 장애물
    spd = 0;
    spd2 = 0;
    analogWrite(9, spd);        //모터 정지
    analogWrite(8, spd2);
    delay(3000);               // 3초 딜레이
    spd2 = 117;
    analogWrite(8, spd2);     // 후진 117rpm
  }
  Serial.print("left = ");      //시리얼모니터에 보이게 함
  Serial.print(ldist);
  Serial.print("  right = ");
  Serial.println(rdist);*/
  Serial.print("angle = ");
  Serial.println(p); 
  Serial.print("dist = ");
  Serial.println(dist);
  Serial.print("spd = ");
  Serial.print(spd);
  Serial.print("  spd2 = ");
  Serial.println(spd2);
  Serial.print("\n");
  delay(500); 
}
