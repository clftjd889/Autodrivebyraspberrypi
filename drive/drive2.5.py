import numpy as np
import cv2
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = None)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

z = 'g'

count = 0

while(True):
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)
    frame = cv2.flip(frame, 1)
    
    blur = cv2.GaussianBlur(frame, (5,5), 0)
    
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv) 
    
    
    #색깔 영역
    
    low_yellow = np.array([8, 50-10, 150-30])
    up_yellow = np.array([60, 255, 255])
    
    low_white = np.array([0, 0, 255-60])
    up_white = np.array([180, 0+54, 255])
    
    low_red = np.array([0, 100, 50])
    up_red = np.array([20, 255, 255])
    
    low_blue = np.array([120-8, 70, 70])
    up_blue = np.array([120+10, 255, 255-50])
    
    yellow_mask = cv2.inRange(hsv, low_yellow, up_yellow)
    yellow = cv2.bitwise_and(hsv, hsv, mask = yellow_mask)
    yellow = cv2.cvtColor(yellow, cv2.COLOR_HSV2BGR)
    
    white_mask = cv2.inRange(hsv, low_white, up_white)
    white = cv2.bitwise_and(hsv, hsv, mask = white_mask)
    white = cv2.cvtColor(white, cv2.COLOR_HSV2BGR)
    
    red_mask = cv2.inRange(hsv, low_red, up_red)
    red = cv2.bitwise_and(hsv, hsv, mask = red_mask)
    red = cv2.cvtColor(red, cv2.COLOR_HSV2BGR)
        
    blue_mask = cv2.inRange(hsv, low_blue, up_blue)
    blue = cv2.bitwise_and(hsv, hsv, mask = blue_mask)
    blue = cv2.cvtColor(blue, cv2.COLOR_HSV2BGR)
    
    
    
    
    
    
    gray_red = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)
    
    gray_blue = cv2.cvtColor(blue, cv2.COLOR_BGR2GRAY)
    
    
    
    #주황색 및 흰색 영역 합치기
        
    yellow_white = cv2.add(yellow, white)
    
    gray = cv2.cvtColor(yellow_white, cv2.COLOR_BGR2GRAY)
    
    kernel_size_row = 3
    kernel_size_col = 3
    kernel = np.ones((3, 3), np.uint8)
    
    erosion_gray = cv2.erode(gray, kernel, iterations=1)
    dilation_gray = cv2.dilate(erosion_gray, kernel, iterations=1)
    
    

    # 모서리 검출
    can = cv2.Canny(dilation_gray, 150, 400, None, 3)
    
    #erosion_gray_red = cv2.erode(gray_red, kernel, iterations=1)
    dilation_gray_red = cv2.dilate(gray_red, kernel, iterations=1)
    
    erosion_gray_blue = cv2.erode(gray_blue, kernel, iterations=1)
    dilation_gray_blue = cv2.dilate(erosion_gray_blue, kernel, iterations=1)
    
    can_red = cv2.Canny(dilation_gray_red, 150, 400, None, 3)
    
    can_blue = cv2.Canny(dilation_gray_blue, 150, 400, None, 3)

    # 관심 구역 설정
    height = can.shape[0]
    rectangle = np.array([[(20, height), (50, 440), (590, 440), (620, height)]])
    mask = np.zeros_like(can)
    cv2.fillPoly(mask, rectangle, 255)
    masked_image = cv2.bitwise_and(can, mask)
    ccan = cv2.cvtColor(masked_image, cv2.COLOR_GRAY2BGR)
    
    rectangle_red = np.array([[(500, 280), (500, 0), (640, 0), (640, 280)]])
    mask_red = np.zeros_like(can_red)
    cv2.fillPoly(mask_red, rectangle_red, 255)
    masked_image_red = cv2.bitwise_and(can_red, mask_red)
    #ccan_red = cv2.cvtColor(masked_image_red, cv2.COLOR_GRAY2BGR)
    
    rectangle_blue = np.array([[(560, 280), (560, 0), (640, 0), (640, 280)]])    
    mask_blue = np.zeros_like(can_blue)
    cv2.fillPoly(mask_blue, rectangle_blue, 255)
    masked_image_blue = cv2.bitwise_and(can_blue, mask_blue)

    
    rectangle_stop_line = np.array([[(220, height), (270, 300), (370, 300), (420, height)]])
    mask_stop_line = np.zeros_like(white)
    cv2.fillPoly(mask_stop_line, rectangle_stop_line, 255)
    masked_image_stop_line = cv2.bitwise_and(white, mask_stop_line)
    

    # 직선 검출
    line_arr = cv2.HoughLinesP(masked_image, 1, np.pi / 180, 20, minLineLength=5, maxLineGap=10)

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
    
    middle = l + r
    ming = cv2.addWeighted(frame, 1, ccan, 1, 0)
    
    cv2.imshow('yellow_white', ming)
    #cv2.imshow('red', masked_image_red)
    #cv2.imshow('white', white)3e
    #cv2.imshow('yellow', yellow)
    #cv2.imshow('dilation_gray', dilation_gray)
    
    #cv2.imshow('ccan', ccan)
    #cv2.imshow('blue', masked_image_blue)
    #cv2.imshow('mask', mask) #ROI 확인용
    
    #print('left = ', l)
    #print('Right = ', r)
    
    #if middle > 60 or middle < -60:
    #    count = 0
    
    if middle < 50 and middle > -50:
        count = 0
    
    
    #servo a ~ k -> c - i
    
    
    if (r >= 0 or middle < -20) and (l != 0):
        if l >= 140:
            s = 'o'
        elif l < 140 and l >= 138 :
            s = 'n'
        elif l < 138 and l >= 136:
            s = 'l'
        elif l < 136 and l >= 130:
            s = 'k'
        elif l < 130 and l >= 124:
            s = 'j'
        elif l < 124 and l >= 100:
            s = 'i'
        elif l < 100 and l > 0:
            s = 'c'
        
        elif l <= -130 :
            s = ']'
        elif l > -130 and l <= -128:
            s = '^'
        elif l > -128 and l <= -126:
            s = '_'
        elif l > -126 and l <= -120:
            s = '`'
        elif l > -120 and l <= -114:
            s = 'a'
        elif l > -114 and l <= -100:
            s = 'b'
        elif l > -100 and l < 0:
            s = 'i'

        
    elif l <= 0 or middle > 20:
        if r <= -140 :
            s = '\\'
        elif r > -140 and r <= -138:
            s = '^'
        elif r > -138 and r <= -136:
            s = '_'
        elif r > -136 and r <= -130:
            s = '`'
        elif r > -130 and r <= -124:
            s = 'a'
        elif r > -124 and r <= -100:
            s = 'b'
        elif r > -100 and r <= 0:
            s = 'i'
            
        elif r >= 130:
            s = 'n'
        elif r < 130 and r >= 128:
            s = 'm'
        elif r < 128 and r >= 126:
            s = 'l'
        elif r < 126 and r >= 120:
            s = 'k'
        elif r < 120 and r >= 114:
            s = 'j'
        elif r < 114 and r >= 100:
            s = 'i'
        elif r < 100 and r >= 0:
            s = 'c'

    #elif l == 0 and r <= -130:
    #    s = 'o'
    #elif r == 0 and l >= 130:
    #    s = '^'
    #elif middle > 100:
    #    s = 'o'        
    #elif middle < -100:
    #    s = '^'    
    elif middle >= -5 and middle <= 5:  #직진        
        s = 'g'
        
    elif middle < -5 and middle >= -8:  #우회전
        s = 'h'
    elif middle < -8 and middle >= -13:
        s = 'i'
    elif middle < -13 and middle >= -20: #여기까지 직선 주행
        s = 'j'

    #elif middle < -20 and middle >= -100:
    #    s = 'n'
        
    elif middle > 5 and middle <= 8:  #좌회전
        s = 'f'
    elif middle > 8 and middle <= 13:
        s = 'e'
    elif middle > 13 and middle <= 20: #여기까지 직선 주행
        s = 'd'

    #elif middle > 20 and middle <= 100:
    #    s = '`'
        

    if l == 0 and r == 0 and count == 0:
        if z == '\\' or z == ']' or z == '^' or z == '_' or z == '`' or z == 'a' or z == 'b' or z == 'c':
            s = '\\'
            
        elif z == 'k' or z == 'l' or z == 'm' or z == 'n' or z == 'o':
            s = 'o'
    
    elif (l == 0 or r == 0) and (count == 0):
        if z == '\\' or z == ']':
            s = '\\'
            
        elif z == 'n' or z == 'o':
            s = 'o'
            
            
    if z == 'n' or z == 'o' or z == '\\' or z == ']':
        if count != 0:
            s = z
        
    height = can.shape[0]
    rectangle_left = np.array([[(20, height), (50, 420), (200, 420), (200, height)]])
    mask_left = np.zeros_like(ccan)
    cv2.fillPoly(mask_left, rectangle_left, 255)
    masked_image_left = cv2.bitwise_and(ccan, mask_left)
    
    height = can.shape[0]
    rectangle_right = np.array([[(200, height), (200, 420), (590, 420), (620, height)]])
    mask_right = np.zeros_like(ccan)
    cv2.fillPoly(mask_right, rectangle_left, 255)
    masked_image_right = cv2.bitwise_and(ccan, mask_right)
        
    if count == 1:
        if z == 'n' or z == 'o' or z == '\\' or z == ']':
            if l != 0 and r != 0:
                if masked_image_left.any() != 0 and masked_image_right() != 0:
                    s = 'g'
                    count = 0
    #cv2.imshow('blue', masked_image_blue)
    #cv2.imshow('red', masked_image_red)
        
    if masked_image_blue.any() != 0:
        print('blue')
        s = 'w'
        
    if masked_image_stop_line.any() != 0 and masked_image_red.any() != 0:
        print('red')
        s = 'r'
    
    if s != z:
        print('left = ', l)
        print('Right = ', r)
        print('middle = ', middle)
        print('s = ', s)
        s = s.encode('utf-8')
        ser.write(s)
        s = s.decode('utf-8')
        
    #print('left = ', l)
    #print('Right = ', r)
    #print('middle = ', middle)


    z = s
    
    if z == 'n' or z == 'o' or z == '\\' or z == ']':
        count == 1

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()








