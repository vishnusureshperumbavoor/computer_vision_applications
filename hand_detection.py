import cv2 
import mediapipe as mp 
import time 

class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.5, model_complexity=1):
        self.mode = mode 
        self.maxHands = maxHands 
        self.detectionCon = detectionCon 
        self.trackCon = trackCon 
        self.model_complexity = model_complexity

        self.mpHands = mp.solutions.hands 
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils 
        self.tipIds = [4,8,12,16,20]

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self,img,handNo=0,draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
                h,w,c = img.shape 
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id,cx,cy])
                #if id == 0:
                #if draw:
                   #cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
            return self.lmList 

    def fingersUp(self):
        fingers = []
        # thump
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 fingers
        for id in range(1,5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers
    
def main():
    pTime = 0 
    cTime = 0
    cap = cv2.VideoCapture(0)

    width = 1280  # Set the desired width
    height = 720  # Set the desired height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)      

    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if lmList != None :
            print(lmList[0])

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime 
        cv2.putText(img,f'FPS:{int(fps)}',(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()