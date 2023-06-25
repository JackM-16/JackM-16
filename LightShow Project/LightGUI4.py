import pygame
import sys
import time

pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

icon = pygame.image.load('Images\IconImage.png') 
pygame.display.set_icon(icon)

pygame.display.set_caption("Light Designer")#caption

######------------Loading Screen------------######
win.fill((185,185,185))
font = pygame.font.SysFont('arial', 35)
text = font.render("Loading...", 1, (0,0,0))
win.blit(text, (5 + int(750/2 - text.get_width()/2), 5 + int(750/2 - text.get_height()/2)))
pygame.display.update()

#time.sleep(5)



import LightGUIDef4 as GuiDef
from LightGUIDef4 import colors as color

#-------Define Variables-------#
clock = pygame.time.Clock()

currentScreen = "sequence"

#-------Define Buttons-------#
fileButton = GuiDef.Button(color.white, 15, color.black,  'File')
editButton = GuiDef.Button(color.white, 15, color.black,  'Edit')
toolsButton = GuiDef.Button(color.white, 15, color.black,  'Tools')
viewButton = GuiDef.Button(color.white, 15, color.black,  'View')
audioButton = GuiDef.Button(color.white, 15, color.black,  'Audio')

layoutScreenButton = GuiDef.Button(color.lightGrey2, 18, color.black,  'Layout')
sequenceScreenButton = GuiDef.Button(color.lightGrey2, 18, color.black,  'Sequence')
runScreenButton = GuiDef.Button(color.lightGrey2, 18, color.black,  'Run')
displayScreenButton = GuiDef.Button(color.lightGrey2, 18, color.black,  'Display')

#-------init Screen Classes-------#
layoutScreen = GuiDef.layoutScreen()
sequenceScreen = GuiDef.sequenceScreen()
runScreen = GuiDef.runScreen()
displayScreen = GuiDef.displayScreen()

#-------Main Window-------#
while True:
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h


    win.fill((125,125,125))

    #-------Define Main menu Button Updates-------#
    pygame.draw.rect(win, color.white, (0,0,screen_w,20),0)
    
    fileButton.updateLoc(0 ,0 , 40, 20 )
    editButton.updateLoc(40 ,0 , 40, 20 )
    toolsButton.updateLoc(80 ,0 , 40, 20 )
    viewButton.updateLoc(120 ,0 , 40, 20 )
    audioButton.updateLoc(160 ,0 , 50, 20 )

    fileButton.draw(win)
    editButton.draw(win)
    toolsButton.draw(win)
    viewButton.draw(win)
    audioButton.draw(win)

    layoutScreenButton.updateLoc(5 ,25 , 80, 25 )
    sequenceScreenButton.updateLoc(90 ,25 , 100, 25 )
    runScreenButton.updateLoc(195 ,25 , 60, 25 )
    displayScreenButton.updateLoc(260, 25, 80, 25)

    layoutScreenButton.draw(win)
    sequenceScreenButton.draw(win)
    runScreenButton.draw(win)
    displayScreenButton.draw(win)

    #Draw Line across screen dividing
    pygame.draw.rect(win, color.black, (0,54,screen_w,2),0)

    if currentScreen == "layout":
        layoutScreen.activeRun(win, screen_w, screen_h)
        layoutScreenButton.draw(win, highLight = [150,150,150])
    if currentScreen == "sequence":
        sequenceScreen.activeRun(win, screen_w, screen_h)
        sequenceScreenButton.draw(win, highLight = [150,150,150])
    if currentScreen == "run":
        runScreen.activeRun(win, screen_w, screen_h)
        runScreenButton.draw(win, highLight = [150,150,150])
    if currentScreen == "display":
        displayScreen.activeRun(win, screen_w, screen_h)
        displayScreenButton.draw(win, highLight = [150,150,150])

    pygame.display.update()




    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.VIDEORESIZE:
            win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
        if currentScreen == "layout":
            layoutScreen.allEvent(event, pos)
        elif currentScreen == "sequence":
            sequenceScreen.allEvent(event, pos)
        elif currentScreen == "run":
            runScreen.allEvent(event, pos)
        elif currentScreen == "display":
            displayScreen.allEvent(event, pos)

    if event.type == pygame.MOUSEMOTION:
        fileButton.highlight = fileButton.isOver(pos)
        editButton.highlight = editButton.isOver(pos)
        toolsButton.highlight = toolsButton.isOver(pos)
        viewButton.highlight = viewButton.isOver(pos)
        audioButton.highlight = audioButton.isOver(pos)

        layoutScreenButton.over = layoutScreenButton.isOver(pos)
        sequenceScreenButton.over = sequenceScreenButton.isOver(pos)
        runScreenButton.over = runScreenButton.isOver(pos)
        displayScreenButton.over = displayScreenButton.isOver(pos)


    if event.type == pygame.MOUSEBUTTONDOWN:
        if layoutScreenButton.isOver(pos) :
            currentScreen = "layout"
        if sequenceScreenButton.isOver(pos) :
            currentScreen = "sequence"
        if runScreenButton.isOver(pos) :
            currentScreen = "run"
        if displayScreenButton.isOver(pos) :
            currentScreen = "display"