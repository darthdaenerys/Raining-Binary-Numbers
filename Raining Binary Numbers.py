# import modules and libraries
import cv2
import random
import numpy as np
import time

# define parameters
width=1280
height=720
text1='0'
text2='1'
green1=(11,245,0)
green2=(10,180,3)
green3=(20,150,10)
slowspeed=4
fastspeed=9
mediumspeed=6
smallsize=0.7
mediumsize=1
largesize=1.2
frameopacity=.9
objectopacity=.8
maxObjects=100
lineType=cv2.LINE_AA
textFont=cv2.FONT_HERSHEY_TRIPLEX
trustval=.8
state:bool=False

# camera setup
class CamSetup:
    def __init__(self):
        global camera
        camera=cv2.VideoCapture(0,cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH,width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
        camera.set(cv2.CAP_PROP_FPS,30)
        camera.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

# get random pixel x-coordinate
def getxPixel():
    return random.randint(0,width)

# get random pixel y-coordinate
def getypixel():
    return random.randint(0,height)

# flip frame funcion
def flipFrame(frame):
    x=cv2.flip(frame,1)
    return x

# color space convertor
def colorSpace(frame):
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame=cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
    return frame

# FPS counter
def showFPS(frame):
    frame[30:70,1100:1230]=(233,12,23)
    cv2.rectangle(frame,(1100,30),(1230,70),(0,255,255),2)
    cv2.putText(frame,str(int(fpsfilter))+' FPS',(1105,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)
    return frame

# setup the mouse event call
def mouseEvent(evnt,X,Y,*args):
    global state
    if evnt==cv2.EVENT_LBUTTONDOWN and X<=100 and Y>=height-50:
        if state==True:
            state=False
        else:
            state=True

# set basic window property
cv2.namedWindow('Raining Binary Numbers',cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Raining Binary Numbers',cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
cv2.setMouseCallback('Raining Binary Numbers', mouseEvent)

# fill xpos with random x coordinates
xpos=[]
for i in range(0,maxObjects):
    xpos.append(getxPixel())

# fill ypos with random y coordinates
ypos=[]
for i in range(0,maxObjects):
    ypos.append(getypixel())

# calculate the current time
t1=time.time()
fpsfilter=30
time.sleep(.1)

# start the camera
CamSetup()

# begin program loop
while True:
    # caluclate the time to process a single frame
    dt=time.time()-t1
    t1=time.time()  #reciprocal of dt is fps
    fpsfilter=fpsfilter*trustval+(1/dt)*(1-trustval)    #trust value in order to stabilize fps display

    # read the frame
    _,frame=camera.read()

    # apply necessary conversions
    frame=colorSpace(frame)
    frame=flipFrame(frame)  

    # generate the object frame
    objectFrame=np.zeros([height,width,3],dtype=np.uint8)

    # draw the objects on the frame
    for i in range(0,maxObjects):
        if i%10==0:
            cv2.putText(objectFrame,text1,(xpos[i],ypos[i]),textFont,smallsize,green1,2,lineType)
        elif i%10==1:
            cv2.putText(objectFrame,text1,(xpos[i],ypos[i]),textFont,mediumsize,green2,2,lineType)
        elif i%10==2:
            cv2.putText(objectFrame,text1,(xpos[i],ypos[i]),textFont,largesize,green3,2,lineType)
        elif i%10==3:
            cv2.putText(objectFrame,text1,(xpos[i],ypos[i]),textFont,smallsize,green1,2,lineType)
        elif i%10==4:
            cv2.putText(objectFrame,text1,(xpos[i],ypos[i]),textFont,mediumsize,green2,2,lineType)
        elif i%10==5:
            cv2.putText(objectFrame,text2,(xpos[i],ypos[i]),textFont,largesize,green3,2,lineType)
        elif i%10==6:
            cv2.putText(objectFrame,text2,(xpos[i],ypos[i]),textFont,smallsize,green1,2,lineType)
        elif i%10==7:
            cv2.putText(objectFrame,text2,(xpos[i],ypos[i]),textFont,mediumsize,green2,2,lineType)
        elif i%10==8:
            cv2.putText(objectFrame,text2,(xpos[i],ypos[i]),textFont,largesize,green1,2,lineType)
        else:
            cv2.putText(objectFrame,text2,(xpos[i],ypos[i]),textFont,mediumsize,green2,2,lineType)

    # increment all 3 category of objects
    for i in range(0,ypos.__len__()):
        if i%3==0:
            ypos[i]+=slowspeed
        elif i%3==1:
            ypos[i]+=mediumspeed
        else:
            ypos[i]+=fastspeed

    # change xpos so that frame looks much more random
    for i in range(0,ypos.__len__()):
        if ypos[i]>height:
            xpos[i]=getxPixel()
            ypos[i]=0

    # Blend the actual frame and object frame
    frame=cv2.addWeighted(frame,frameopacity,objectFrame,objectopacity,0)

    # If state is True show FPS counter
    if state:
        frame=showFPS(frame)
    
    # Draw the Toggle ON/OFF switch
    if state:
        cv2.rectangle(frame,(0,height-50),(100,height),(22, 219, 38),-1)
        cv2.putText(frame,'ON',(14,height-8),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)
    else:
        cv2.rectangle(frame,(0,height-50),(100,height),(12, 12, 199),-1)
        cv2.putText(frame,'OFF',(6,height-8),cv2.FONT_HERSHEY_PLAIN,3,(0,0,0),3)

    # output the processed frame
    cv2.imshow('Raining Binary Numbers',frame)
    if cv2.waitKey(1) & 0xff==ord('q'):
        break

cv2.destroyAllWindows()
camera.release()