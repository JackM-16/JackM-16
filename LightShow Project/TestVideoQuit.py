####import cv2
####
####cap = cv2.VideoCapture(1)
####
##### Check if the webcam is opened correctly
####if not cap.isOpened():
####    raise IOError("Cannot open webcam")
####
####while True:
####    ret, frame = cap.read()
####    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
####    cv2.imshow('Input', frame)
####
####    c = cv2.waitKey(1)
####    if c == 27:
####        break
####
####cap.release()
####cv2.destroyAllWindows()

import pygame
import pygame.camera

pygame.init()

gameDisplay = pygame.display.set_mode((1280,720), pygame.RESIZABLE)

pygame.camera.init()
cam = pygame.camera.Camera(0,(1280,720))
cam.start()
while True:
    img = cam.get_image()
    gameDisplay.blit(img,(0,0))
    pygame.display.update()
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            cam.stop()
            pygame.quit()
            exit()
