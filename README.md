# Autodrivebyraspberrypi

https://youtu.be/Z6SSDc6e2hI?si=S2PDZ901VrR8P9o5

2022년 1학기 제주대학교 학부생 캡스톤

자율주행 버스(Autodrive_bus)

파이썬 코드 이용, OPEN_CV 이용, 아두이노와 라즈베리파이의 연계


이미지 처리는 open_cv를 설치한 라즈베리파이에서 파이썬 코드로 실행, 카메라를 통해서 받아오는 이미지의 일정 부분에서 직선 검출, 그 직선의 각도 도출, 검출되는 직선 두 개(차선)의 각도를 빼서 하나의 직선으로 결정, 이를 통해 직진, 좌회전, 우회전 결정.

카메라 위치나 이미지의 딜레이에 따른 유동적인 값들은 시행착오를 통해 보정값으로 더해 제작.

라즈베리 파이에서 이미지 처리 후 정보를 아두이노로 보내서 구동. 구동은 서보모터, 모터(전동기)를 사용.

모터의 힘과 전지 용량은 예상 중량을 산정하여 결정, 기계적으로 결합이 완벽하지 않아서 생긴 오차는 시행착오를 통해 보정값으로 보완.
