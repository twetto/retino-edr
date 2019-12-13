#!/usr/bin/python3
import numpy as np
import cv2
import time

#cap = cv2.VideoCapture('VID_20191212_204303.mp4')
#writer = cv2.VideoWriter('output.mkv',cv2.VideoWriter_fourcc('X','2','6','4'),60,(640,360))
cap = cv2.VideoCapture(0 + cv2.CAP_V4L2)
ret, p_ema = cap.read()
p_ema = cv2.cvtColor(p_ema,cv2.COLOR_BGR2GRAY)
#p_ema = cv2.resize(p_ema,(640,360))
float_p_ema = np.float32(p_ema)

while(True):
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #frame = cv2.resize(frame,(640,360))
    float_frame = np.float32(frame)
    #ema = (p_ema >> 1) + (frame >> 1)
    
    float_ema = float_p_ema * 0.167 + float_frame * 0.833
    r = np.log(float_frame / float_ema)
    on = r - 0.02
    off = -0.02 - r
    on = 255 * (on > 0)
    off = 255 * (off > 0)
    on = np.uint8(on)
    off = np.uint8(off)
    #on = cv2.cvtColor(on,cv2.COLOR_BGR2GRAY)
    on = cv2.cvtColor(on,cv2.COLOR_GRAY2BGR)
    on[:,:,0] = 0
    on[:,:,1] = 0
    #off = cv2.cvtColor(off,cv2.COLOR_BGR2GRAY)
    off = cv2.cvtColor(off,cv2.COLOR_GRAY2BGR)
    off[:,:,0] = 0
    off[:,:,2] = 0
    edr = on + off
    cv2.imshow('EDR',edr)
    #writer.write(edr)

    #cv2.imshow('EMA',ema)
    cv2.imshow('frame',frame)
    float_p_ema = float_ema
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        time.sleep(10)

cap.release()
cv2.destroyAllWindows()

