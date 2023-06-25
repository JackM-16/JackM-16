import pygame
import sys
import os
import time
import LightGuiDef
#import SerialTrackless

pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h

#-------Define Colors-------#
red = (150,0,0)
lightRed = (255,0,0)
orange = (255,150,0)
green = (0,200,0)
light_green = (0,255,0)
blue = (0,0,200)
purple = (144,34,199)
brown = (117,79,45)
black = (0,0,0)
white = (255,255,255)
lightGrey2 = (185,185,185)
lightGrey = (100,100,100)
darkGrey = (50,50,50)

#background/title
win.fill((225,0,0))  # Fills the screen with what ever color

pygame.display.set_caption("Light GUI")#caption

#-------Define Variables-------#
clock = pygame.time.Clock()
startScreen = False
fullscreen = False
currentScreen = "LAYOUT"

#-------Define Buttons-------#
layoutButton = LightGuiDef.Button((darkGrey), 20, white,  'LAYOUT')
sequenceButton = LightGuiDef.Button((darkGrey), 20, white,  'SEQUENCE')
renderButton = LightGuiDef.Button((darkGrey), 20, white,  'RENDER')

addLineButton = LightGuiDef.Button((darkGrey), 17, white,  'Line')
addCircleButton = LightGuiDef.Button((darkGrey), 15, white,  'Circle')
addPolylineButton = LightGuiDef.Button((darkGrey), 17, white,  'Poly')



#-------Test Objects-------#
drawScreenLayout = LightGuiDef.Button((lightGrey), 15, white,  '')
testListBox = LightGuiDef.listBox((0,0,150),25,(0,0,0),["0","1","2","3","4","5","6","7","8","9",'10','11','12','13'])
testListBoxDown = LightGuiDef.listBox((0,0,150),25,(0,0,0),["1","1","2","3","4","5","6","7","8","9",'10','11','12','13',"1","2","3","4","5","6","7","8"])

while True:
    win.fill((lightGrey2))
    
    keys = pygame.key.get_pressed()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h

    #-------Define Buttons Updates-------# 
    layoutButton.updateLoc(5 , 5 , 75, 30 )
    sequenceButton.updateLoc(85 , 5 , 75, 30 )
    renderButton.updateLoc(165 , 5 , 75, 30 )

    addLineButton.updateLoc(295 , 40 , 30, 30 )
    addCircleButton.updateLoc(330 , 40 , 30, 30 )
    addPolylineButton.updateLoc(365, 40, 30, 30)
    
    #-------Test Objects Updates-------#
    drawScreenLayout.updateLoc(295 , 75 , screen_w-300,screen_h-80)
    testListBox.updateLoc(5,40,285,295-5)
    testListBoxDown.updateLoc(5,40+300,285,screen_h-345)
    
    #-------Get Mouse and Keys-------# 
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()
            
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_f]:
            fullscreen = not fullscreen
            if fullscreen:
                win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

    #-------Draw Main Objects-------# 
    layoutButton.draw(win, ())
    sequenceButton.draw(win, ())
    renderButton.draw(win, ())
    if currentScreen == "LAYOUT":
        layoutButton.shadow(win)
    elif currentScreen == "SEQUENCE":
        sequenceButton.shadow(win)
    elif currentScreen == "RENDER":
        renderButton.shadow(win)

    #-------Hover/Click Main Objects-------# 
    if event.type == pygame.MOUSEMOTION:
        if layoutButton.isOver(pos):
            layoutButton.draw(win, (white))
        else:
            layoutButton.draw(win, ())
        if sequenceButton.isOver(pos):
            sequenceButton.draw(win, (white))
        else:
            sequenceButton.draw(win, ())
        if renderButton.isOver(pos):
            renderButton.draw(win, (white))
        else:
            renderButton.draw(win, ())

    if event.type == pygame.MOUSEBUTTONDOWN:
        if layoutButton.isOver(pos):
            currentScreen = "LAYOUT"
            pygame.time.wait(250)
        #else:
            #layoutButton.draw(win, ())
        if sequenceButton.isOver(pos):
            currentScreen = "SEQUENCE"
            pygame.time.wait(250)
        #else:
            #sequenceButton.draw(win, ())
        if renderButton.isOver(pos):
            currentScreen = "RENDER"
            pygame.time.wait(250)
        #else:
            #renderButton.draw(win, ())

##                
    if currentScreen == "LAYOUT":
        addLineButton.draw(win, ())
        addCircleButton.draw(win, ())
        addPolylineButton.draw(win, ())

        drawScreenLayout.draw(win, ())
        testListBox.draw(win, ())
        testListBox.eventHandler(event)
        #testListBoxDown.draw(win, ())
##        if drawPictureRemove == True:
####        picture2 = pygame.image.load("C:/Users/jtmti/Downloads/IMG_0403.jpg")
####        #picture = pygame.transform.rotate(picture2, -90)
####        picture = pygame.transform.scale(   picture2, (int(screen_w-300), int(screen_h-80))    )
####        rect = picture.get_rect()
####        rect = rect.move((295, 75))
####        win.blit(picture, rect)

        
##        pygame.draw.rect(win, (100,0,100), (400,200,400,400),0)
##        
##        selectedLightLineList = connectionsItemArray.returnClickedItems()
##        designButton.shadow(win)
##        addLineButton.draw(win)
##
##        #Buttons only in this screen
##        if event.type == pygame.MOUSEMOTION:
##            connectionsItemArray.hoverChangeSelected(pos, win)
##            if addLineButton.isOver(pos):
##                addLineButton.draw(win, (white))
##            else:
##                addLineButton.draw(win, ())
##
##        if event.type == pygame.MOUSEBUTTONDOWN:
##            connectionsItemArray.clickScroll(pos)
##            connectionsItemArray.clickItems(pos)
##            connectionsItemArray.clickChangeSelected(pos)
##            
##            if addBackGroundButton.isOver(pos):
##                pygame.time.wait(100)
##  
    pygame.display.update()
    

