import cv2
import mediapipe as mp
import time
mpDraw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
cap =cv2.VideoCapture(0)
pT = 0 
while True:
   success, img = cap.read()
   imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
   results = pose.process(imgRGB)
   #print(results.pose_landmarks)
   if results.pose_landmarks:
       mpDraw.draw_landmarks(img,results.pose_landmarks,mpPose.POSE_CONNECTIONS )
       for id,lm in enumerate(results.pose_landmarks.landmark):
           h,w,c=img.shape
           cx, cy =int(lm.x*w),int(lm.y*h)
           cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
           #print(id, cx, cy)
   cT =time.time()
   fps = 1/(cT-pT)
   pT = cT
   cv2.putText(img, str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
   cv2.imshow("VSP Pose Estimation",img)
   if cv2.waitKey(10) == ord('q'):
        break 