import numpy as np
import cv2
import threading

camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)
camera3 = cv2.VideoCapture(2)

activeCamera=1

def make_1080p(camera):
    camera.set(3, 1920)
    camera.set(4, 1080)

def make_720p(camera):
    camera.set(3, 1280)
    camera.set(4, 720)

def make_480p(camera):
    camera.set(3, 640)
    camera.set(4, 480)

def change_res(camera,width, height):
    camera.set(3, width)
    camera.set(4, height)
    
def rescale_frame(frame, width1, height2):
    width = int(width1)
    height = int(height2)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

make_720p(camera1)
make_720p(camera2)
make_720p(camera3)

inWidth = 1
inHeight = 1

while True:
    ret, frameCamera1 = camera1.read()
    ret, frameCamera2 = camera2.read()
    ret, frameCamera3 = camera3.read()
    
    if activeCamera==1: 
        ret, frame = camera1.read()
        inWidth = 1280
        inHeight = 720
        width_camera = int(camera1.get(3))
        height_camera = int(camera1.get(4))
        set_FPS = 1
    if activeCamera==2: 
        ret, frame = camera2.read()
        inWidth = 960
        inHeight = 720
        width_camera = int(camera2.get(3))
        height_camera = int(camera2.get(4))
        set_FPS = 1
    if activeCamera==3: 
        ret, frame = camera3.read()
        inWidth = 1280
        inHeight = 720
        width_camera = int(camera2.get(3))
        height_camera = int(camera2.get(4))
        #set_FPS = 30

    frame = rescale_frame(frame, inWidth, inHeight)
##    frameCamera1 = rescale_frame(frameCamera1, inWidth, inHeight)
##    frameCamera2 = rescale_frame(frameCamera2, inWidth, inHeight)
##    frameCamera3 = rescale_frame(frameCamera3, inWidth, inHeight)
##    
##    image = np.zeros(frame.shape, np.uint8)
##    smaller_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
##    smaller_frame1 = cv2.resize(frameCamera1, (0,0), fx=0.5, fy=0.5)
##    smaller_frame2 = cv2.resize(frameCamera2, (0,0), fx=0.5, fy=0.5)
##    smaller_frame3 = cv2.resize(frameCamera3, (0,0), fx=0.5, fy=0.5)
##    
##    image[:height_camera//2, :width_camera//2] = smaller_frame
##    image[height_camera//2:, :width_camera//2] = smaller_frame1
##    image[:height_camera//2, width_camera//2:] = smaller_frame2
##    image[height_camera//2:, width_camera//2:] = smaller_frame3
##    
##    
##    cv2.imshow('frame', image)

    frame2 = rescale_frame(frame, 1920, 1080)
    cv2.imshow('frame2', frame2)
    
    keyPressed = cv2.waitKey(set_FPS)
    
    if keyPressed == ord('q'):
        break
    if keyPressed == ord('a'):
        activeCamera=1
    if keyPressed == ord('s'):
        activeCamera=2
    if keyPressed == ord('d'):
        activeCamera=3

camera1.release()
camera2.release()
camera3.release()
cv2.destroyAllWindows()

