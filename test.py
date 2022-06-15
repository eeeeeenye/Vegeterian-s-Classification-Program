from operator import index
from threading import Thread
import cv2
#import pytesseract as pt
import re
import DBmanager as db
import webParsing as wp
import visionAPI as ocr


Dragging = False                         # 마우스 드래그 상태 저장 
x0, y0, w, h = 0,0,0,0                   # 영역 선택 좌표 저장
green, red = (0,255,0),(0,0,255)         # 색상 값
ingr = []
C_meterials = []                         # 비교할 원재료
flag = 0

Url = ""

def mouse_event(event,x,y,flags,param):  # 마우스 제어함수
    global Dragging, x0, y0, flag,Url

    img = cv2.imread(Url,cv2.IMREAD_COLOR)
#    dst = cv2.resize(img, dsize=(800,800), interpolation=cv2.INTER_LINEAR) 

    if event == cv2.EVENT_LBUTTONDOWN :
        Dragging = True
        x0,y0 = x,y                      # 마우스 왼쪽 버튼을 눌렀을 때의 x,y 좌표 저장
    elif event == cv2.EVENT_MOUSEMOVE :  # 마우스가 왼쪽 버튼을 누른 이후 움직일 때 -> 사각형의 크기설정
        if Dragging == True :  
            imgDraw = img.copy()
            cv2.rectangle(imgDraw,(x0,y0),(x,y),green,5)
            cv2.imshow('img',imgDraw)
    elif event == cv2.EVENT_LBUTTONUP :
          Dragging = False
          w = x - x0                     # 사각형의 width
          h = y - y0                     # 사각형의 height
          if w > 0 and h > 0 :           # 값이 모두 양수라면 true
            img_draw = img.copy()        # 선택 영역에 사각형 그림을 표시할 이미지 복제
            cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2) 
            cv2.imshow('img', img_draw)  # 빨간 사각형 그려진 이미지 화면 출력
            roi = img[y0:y0+h, x0:x0+w]  # 원본 이미지에서 선택 영역만 ROI로 지정
            cv2.imshow('new_img', roi)   # ROI 지정 영역을 새창으로 표시
            cv2.destroyWindow('img')
            cv2.moveWindow('new_img', 150, 150)
            cv2.imwrite('./image/new_img.jpg', roi) # ROI 영역만 파일로 저장
            img2text('./image/new_img.jpg')
            cv2.destroyWindow('new_img')
    else:
        cv2.imshow('img', img)           # 드래그 방향이 잘못된 경우 사각형 그림이 없는 원본 이미지 출력

def img2text(str):
#    str = pt.image_to_string(str, lang='kor')
    global ingr
    text = ocr.vision(str)
    print(text)

    text = text.replace('[',')').replace(']',')') # [] 을 ()로 바꿔줌
    ingr = re.split('[-|.|(|}|)|*|{|:|;|,|0-9|/|\n|%|$]',text) #구분자를 정해 str에 있는 특수문자별로 분할
    ingr = list(filter(None,ingr))
    print(ingr)

def compare():                                             # 비교 순서 1. 락토 2. 락토오보 3. 페스코 4. 폴로 5.논채식
    result = ''
    global ingr,C_meterials
    novege,Pcount, LOcount, Lcount, POcount = 0,0,0,0,0    # 카운터를 통해 채식 단계를 분류함
    num = 0

    while True:
        list_ = db.dataInput(num)
        C_meterials = list(map(list, list_))                # 튜플을 리스트로 변환
        C_meterials = sum(C_meterials,[])                   # 변환된 이차원 리스트를 하나로 병합
        redun_c = list(set(ingr).intersection(C_meterials))   # 리스트와 리스트 사이 중복값 redun_c에 저장
        
        if len(redun_c) > 0 :
            if num==0:
                Lcount += 1
            elif num==1:
                LOcount += 1
            elif num==2:
                Pcount += 1
            elif num==3:
                POcount += 1
            elif num==4:
                novege += 1

        if num > 4:
            break

        num += 1
            
    if novege > 0:
        Pcount, LOcount, Lcount, POcount = 0,0,0,0
        result = '비채식' 
    elif POcount > 0:
        result = '폴로베지테리안'
    elif Pcount > 0:
        result = '페스코베지테리안'
    elif LOcount > 0 :
        result = '락토오보'
    elif Lcount > 0 :
        result = '락토'
    else:
        result = '비건'

    return result


def main(url):
    global Url
    Url = url

    img = cv2.imread(Url,cv2.IMREAD_COLOR)
#    dst2 = cv2.resize(img, dsize=(800,500), interpolation=cv2.INTER_AREA)   
    cv2.imshow('img', img)
    cv2.setMouseCallback('img', mouse_event) # 마우스 이벤트 등록
    cv2.waitKey()
    cv2.destroyAllWindows()
    result = compare()
    print(result)
    return result


API = wp.APIparser() # 제출 시 주석없애고
API.start()


