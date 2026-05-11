import cv2
import mediapipe as mp
import pyautogui
from scipy.spatial import distance

mS = False
ms_P = False
click = False
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
pyautogui.PAUSE = 0
index_x, index_y = 50,50
indexPos = [0,0]
middlePos = [0,0]

a = False
b = False
c = False
d = False

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)

    hands = output.multi_hand_landmarks 
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand) # 손에 20개의 점 표시
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width) # 점의 카메라상의 x좌표 환산
                y = int(landmark.y*frame_height) # 점의 카메라상의 y좌표 환산

                if id == 8: # 8번째 점(검지손가락 끝점)이 감지되었다면
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255)) # 화면 상에 8번째 점(검지손가락 끝점) 표시
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    indexPos = [index_x,index_y]
                    
                     # 마우스 커서 위치를 8번째 점으로 이동

                if id == 12:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 0))
                    middle_x = screen_width/frame_width*x
                    middle_y = screen_height/frame_height*y
                    middlePos = [middle_x, middle_y]


                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(255, 0, 0))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    pyautogui.moveTo(thumb_x, thumb_y)
                    thumbPos = [thumb_x, thumb_y]
                    #print(thumb_x, thumb_y)
                    thumbIndexD = distance.euclidean(thumbPos, indexPos)
                    #print(thumbIndexD)
                    middleIndexD = distance.euclidean(middlePos, thumbPos)
                    #print(middleIndexD)
                    #thumbIndexD = distance.euclidean(thumbPos, indexPos)
                    
                    if thumbIndexD < 70:
                        a = True
                        if a != b:
                            b=a
                            pyautogui.keyDown("e")
                        pyautogui.keyUp("e")
                    elif 70 <= thumbIndexD < 500:
                        b = False
                        a = False

                    if middleIndexD < 70: 
                        pyautogui.keyDown("s")
                        
                    elif 70 <= middleIndexD < 500:
                        pyautogui.keyUp("s")

                            
                    

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)