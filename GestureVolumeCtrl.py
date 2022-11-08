import cv2
import numpy as np
import time
import HandTrackingmod as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
Wcam, Hcam = 640, 460
cTime, pTime = 0, 0
cap = cv2.VideoCapture(0)
cap.set(3, Wcam)
cap.set(4, Hcam)
detector = htm.handDetector()
# detector.detectionCon = 0.7
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
print(volRange)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    isTrue, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist) != 0:
        # print(lmlist[4], lmlist[8])
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cv2.circle(img, (x1, y1), 10, (225, 0, 225), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (225, 0, 225), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (225, 0, 225), 3)
        cv2.circle(img, ((x1+x2)//2, (y1+y2)//2), 10, (225, 0, 225), cv2.FILLED)
        length = math.hypot((x2-x1), (y2-y1))
        # print(length)
        # Hand range 50 - 200
        # Volume Range -63.5 - 0.0
        vol = np.interp(length, [50, 200], [minVol, maxVol])#
        # Volume Bar- 400-150
        volBar = np.interp(length, [50, 200], [400, 150])
        #Original Volume - 0-100
        volPer = np.interp(length, [50, 200], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length<50:
            cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 10, (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 225, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0XFF == ord('s'):
        break
