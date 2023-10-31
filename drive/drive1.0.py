import numpy as np
import cv2
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)



while(True):
    ret, frame = cap.read()
    #blur = cv2.GaussianBlur(frame, (5,5), 0)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    #색깔 영역
    
    low_yellow = np.array([8, 50, 150])
    up_yellow = np.array([60, 255, 255])
    
    low_white = np.array([0, 0, 255-75])
    up_white = np.array([180, 0+75, 255])
    
    yellow_mask = cv2.inRange(hsv, low_yellow, up_yellow)
    yellow = cv2.bitwise_and(hsv, hsv, mask = yellow_mask)
    yellow = cv2.cvtColor(yellow, cv2.COLOR_HSV2BGR)
    
    white_mask = cv2.inRange(hsv, low_white, up_white)
    white = cv2.bitwise_and(hsv, hsv, mask = white_mask)
    white = cv2.cvtColor(white, cv2.COLOR_HSV2BGR)
    
    #주황색 및 흰색 영역 합치기
        
    yellow_white = cv2.add(yellow, white)
    
    gray = cv2.cvtColor(yellow_white, cv2.COLOR_BGR2GRAY)

    # 모서리 검출
    can = cv2.Canny(gray, 150, 400, None, 3)

    # 관심 구역 설정
    height = can.shape[0]
    rectangle = np.array([[(0, height), (80, 250), (560, 250), (640, height)]])
    mask = np.zeros_like(can)
    cv2.fillPoly(mask, rectangle, 255)
    masked_image = cv2.bitwise_and(can, mask)
    ccan = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)

    # 직선 검출
    line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20, minLineLength=10, maxLineGap=10)

    # line color
    # color = [0, 0, 255]
    # thickness = 5
    # for line in line_arr:
    #   for x1, y1, x2, y2 in line:
    #        cv2.line(ccan, (x1, y1), (x2, y2), color, thickness)

    # 중앙을 기준으로 오른쪽, 왼쪽 직선 분리
    line_R = np.empty((0, 5), int)
    line_L = np.empty((0, 5), int)
    if line_arr is not None:
        line_arr2 = np.empty((len(line_arr), 5), int)
        for i in range(0, len(line_arr)):
            temp = 0
            l = line_arr[i][0]
            line_arr2[i] = np.append(line_arr[i], np.array((np.arctan2(l[1] - l[3], l[0] - l[2]) * 180) / np.pi))
            if line_arr2[i][1] > line_arr2[i][3]:
                temp = line_arr2[i][0], line_arr2[i][1]
                line_arr2[i][0], line_arr2[i][1] = line_arr2[i][2], line_arr2[i][3]
                line_arr2[i][2], line_arr2[i][3] = temp
            if line_arr2[i][0] < 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                line_L = np.append(line_L, line_arr2[i])
            elif line_arr2[i][0] > 320 and (abs(line_arr2[i][4]) < 170 and abs(line_arr2[i][4]) > 95):
                line_R = np.append(line_R, line_arr2[i])
    line_L = line_L.reshape(int(len(line_L) / 5), 5)
    line_R = line_R.reshape(int(len(line_R) / 5), 5)

    # 중앙과 가까운 오른쪽, 왼쪽 선을 최종 차선으로 인식
    try:
        line_L = line_L[line_L[:, 0].argsort()[-1]]
        degree_L = line_L[4]
        cv2.line(ccan, (line_L[0], line_L[1]), (line_L[2], line_L[3]), (255, 0, 0), 10, cv2.LINE_AA)
    except:
        degree_L = 0
    try:
        line_R = line_R[line_R[:, 0].argsort()[0]]
        degree_R = line_R[4]
        cv2.line(ccan, (line_R[0], line_R[1]), (line_R[2], line_R[3]), (255, 0, 0), 10, cv2.LINE_AA)
    except:
        degree_R = 0
        
    l, r = degree_L, degree_R
    
    m = l + r
    
    ming = cv2.addWeighted(frame, 1, ccan, 1, 0)
    
    cv2.imshow('yellow_white', ming)
    cv2.imshow('white', white)
    
    
    print('left = ', l)
    print('Right = ', r)    
    print('middle = ', m)
    
    
    #servo a ~ k -> c - i
    
    if m >= -10 and m <= 10:
        s = 'f'
    elif l == 0 and r <= -140:
        s = 'b'
    elif r == 0 and l >= 140:
        s = 'j'
    elif m > 10 and m <= 20:
        s = 'g'
    elif m < -10 and m >= -20:
        s = 'e'
    elif m > 20 and m <= 30:
        s = 'h'
    elif m < -20 and m >= -30:
        s = 'd'
    elif m > 30:
        s = 'c'
    elif m < -30:
        s = 'i'
        
    print('s = ', s)
    
    s = s.encode('utf-8')
    ser.write(s)    
    
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()

