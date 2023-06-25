import pygame
import sys
import os

pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

pygame.display.set_caption("Light Navigator")#caption
######------------Loading Screen------------######
win.fill((185,185,185))
font = pygame.font.SysFont('arial', 35)
text = font.render("Loading...", 1, (0,0,0))
win.blit(text, (5 + int(750/2 - text.get_width()/2), 5 + int(750/2 - text.get_height()/2)))
pygame.display.update()

import LightGUI3Def as GuiDef
import easygui
import time
import threading
import SerialCsvTest as PixelWrite
import ReadWriteDef as NumUpdate
import PixelEffects

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



#-------Define Variables-------#
clock = pygame.time.Clock()
fullscreen = False

mainScreenMode = "layout"

mainMenuTopIndex = -1
mouseScreenOverride = False
menuLastCheckOveride = 0

#-------Define Buttons-------#
fileButton = GuiDef.Button(white, 15, black,  'File')
editButton = GuiDef.Button(white, 15, black,  'Edit')
toolsButton = GuiDef.Button(white, 15, black,  'Tools')
viewButton = GuiDef.Button(white, 15, black,  'View')
audioButton = GuiDef.Button(white, 15, black,  'Audio')

layoutScreenButton = GuiDef.Button(lightGrey2, 15, black,  'Layout')
sequenceScreenButton = GuiDef.Button(lightGrey2, 15, black,  'Sequence')
runScreenButton = GuiDef.Button(lightGrey2, 15, black,  'Run')

#-------Menu Top Buttons---------#
file_NewButton = GuiDef.Button(white, 15, black,  'New File')
file_OpenButton = GuiDef.Button(white, 15, black,  'Open')
file_SaveButton = GuiDef.Button(white, 15, black,  'Save')
file_SaveAsButton = GuiDef.Button(white, 15, black,  'Save As')
file_QuitButton = GuiDef.Button(white, 15, black,  'Quit')

edit_UndoButton = GuiDef.Button(white, 15, black,  'Undo')
edit_CutButton = GuiDef.Button(white, 15, black,  'Cut')
edit_CopyButton = GuiDef.Button(white, 15, black,  'Copy')
edit_PasteButton = GuiDef.Button(white, 15, black,  'Paste')

tools_TestButton = GuiDef.Button(white, 15, black,  'Test')
tools_RenderButton = GuiDef.Button(white, 15, black,  'Render')
tools_AddBackgroundButton = GuiDef.Button(white, 15, black,  'Add Background')
tools_ConnectButton = GuiDef.Button(white, 15, black,  'Connect')

view_FullScreenButton = GuiDef.Button(white, 15, black,  'Full Screen')
view_WindowScreenButton = GuiDef.Button(white, 15, black,  'Window Screen')
view_ZoomInButton = GuiDef.Button(white, 15, black,  'Zoom In')
view_ZoomOutButton = GuiDef.Button(white, 15, black,  'Zoom Out')

audio_FullSpeedButton = GuiDef.Button(white, 15, black,  'Play Full Speed')
audio_HalfSpeedButton = GuiDef.Button(white, 15, black,  'Play 1/2 Speed')
audio_OneHalfSpeedButton = GuiDef.Button(white, 15, black,  'Play 1.5x Speed')
audio_TwoSpeedButton = GuiDef.Button(white, 15, black,  'Play 2x Speed')
audio_ThreeSpeedButton = GuiDef.Button(white, 15, black,  'Play 3x Speed')
audio_FourSpeedButton = GuiDef.Button(white, 15, black,  'Play 4x Speed')

#-------Define Screen Classes-------#
layoutScreenDef = GuiDef.layoutScreen()
sequenceScreenDef = GuiDef.sequenceScreen()

while True:
    win.fill((225,225,225))
    
    keys = pygame.key.get_pressed()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h

    #-------Define Button Updates-------#
    pygame.draw.rect(win, white, (0,0,screen_w,20),0)
    
    fileButton.updateLoc(0 ,0 , 40, 20 )
    editButton.updateLoc(40 ,0 , 40, 20 )
    toolsButton.updateLoc(80 ,0 , 40, 20 )
    viewButton.updateLoc(120 ,0 , 40, 20 )
    audioButton.updateLoc(160 ,0 , 50, 20 )

    layoutScreenButton.updateLoc(3 ,93 , 60, 20 )
    sequenceScreenButton.updateLoc(66 ,93 , 80, 20 )
    runScreenButton.updateLoc(149 ,93 , 40, 20 )

    #-------Draw Buttons-------#
    fileButton.draw(win)
    editButton.draw(win)
    toolsButton.draw(win)
    viewButton.draw(win)
    audioButton.draw(win)

    pygame.draw.rect(win, [150,150,150], (0,20,screen_w,70),0) ##Top Line Background

    pygame.draw.rect(win, [150,150,150], (0,116,screen_w,2),0) ##Line dividing diffrent tebs


    if mainScreenMode == "layout":
        layoutScreenDef.draw(win, screen_w, screen_h)
        layoutScreenButton.draw(win, highLight = [150,150,150])
        sequenceScreenButton.draw(win)
        runScreenButton.draw(win)
        
    if mainScreenMode == "sequence":
        sequenceScreenDef.draw(win, screen_w, screen_h)
        layoutScreenButton.draw(win)
        sequenceScreenButton.draw(win, highLight = [150,150,150])
        runScreenButton.draw(win)
        
    if mainScreenMode == "run":
        layoutScreenButton.draw(win)
        sequenceScreenButton.draw(win)
        runScreenButton.draw(win, highLight = [150,150,150])
        

    
    #-------Get Mouse and Keys-------# 
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            LightModeThread = "stop"
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if keys[pygame.K_q]:
            LightModeThread = "stop"
            pygame.quit()
            sys.exit()
            
        if keys[pygame.K_ESCAPE]:
            LightModeThread = "stop"
            pygame.quit()
            sys.exit()

        #if keys[pygame.K_f]:
        #    fullscreen = not fullscreen
        #    if fullscreen:
        #        win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
        #    else:
        #        win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

        if mouseScreenOverride == False:
            if mainScreenMode == "layout":
                layoutScreenDef.eventHandler(event)
            if mainScreenMode == "sequence":
                sequenceScreenDef.eventHandler(event)

    if event.type == pygame.MOUSEMOTION:
        if fileButton.isOver(pos):
            fileButton.draw(win, highLight = [148,192,255])
        else:
            fileButton.draw(win)
        if editButton.isOver(pos):
            editButton.draw(win, highLight = [148,192,255])
        else:
            editButton.draw(win)
        if toolsButton.isOver(pos):
            toolsButton.draw(win, highLight = [148,192,255])
        else:
            toolsButton.draw(win)
        if viewButton.isOver(pos):
            viewButton.draw(win, highLight = [148,192,255])
        else:
            viewButton.draw(win)
        if audioButton.isOver(pos):
            audioButton.draw(win, highLight = [148,192,255])
        else:
            audioButton.draw(win)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if mouseScreenOverride == False:
            if layoutScreenButton.isOver(pos):
                mainScreenMode = "layout"
            if sequenceScreenButton.isOver(pos):
                mainScreenMode = "sequence"
            if runScreenButton.isOver(pos):
                mainScreenMode = "run"
                

        if fileButton.isOver(pos) :
            mainMenuTopIndex = 0
        elif editButton.isOver(pos):
            mainMenuTopIndex = 1
        elif toolsButton.isOver(pos):
            mainMenuTopIndex = 2
        elif viewButton.isOver(pos):
            mainMenuTopIndex = 3
        elif audioButton.isOver(pos):
            mainMenuTopIndex = 4
        else:
            menuLastCheckOveride = -1



    if mainMenuTopIndex > -1:
        mouseScreenOverride = True
        if mainMenuTopIndex == 0:
            pygame.draw.rect(win, [200,200,200], (0,20,160,112),0)
            fileButton.color = [148,192,255]
            
            file_NewButton.updateLoc(2 ,22 , 156, 20 )
            file_OpenButton.updateLoc(2 ,44 , 156, 20 )
            file_SaveButton.updateLoc(2 ,66 , 156, 20 )
            file_SaveAsButton.updateLoc(2 ,88 , 156, 20 )
            file_QuitButton.updateLoc(2 ,110 , 156, 20 )

            file_NewButton.draw(win)
            file_OpenButton.draw(win)
            file_SaveButton.draw(win)
            file_SaveAsButton.draw(win)
            file_QuitButton.draw(win)

            if event.type == pygame.MOUSEMOTION:
                if file_NewButton.isOver(pos):
                    file_NewButton.draw(win, highLight = [0,120,225])
                if file_OpenButton.isOver(pos):
                    file_OpenButton.draw(win, highLight = [0,120,225])
                if file_SaveButton.isOver(pos):
                    file_SaveButton.draw(win, highLight = [0,120,225])
                if file_SaveAsButton.isOver(pos):
                    file_SaveAsButton.draw(win, highLight = [0,120,225])
                if file_QuitButton.isOver(pos):
                    file_QuitButton.draw(win, highLight = [0,120,225])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if file_NewButton.isOver(pos):
                    print("New")
                if file_OpenButton.isOver(pos):
                    print("Open")
                if file_SaveButton.isOver(pos):
                    print("Save")
                if file_SaveAsButton.isOver(pos):
                    print("Save As")
                if file_QuitButton.isOver(pos):
                    LightModeThread = "stop"
                    pygame.quit()
                    sys.exit()

        else:
            fileButton.color = white

        if mainMenuTopIndex == 1:
            pygame.draw.rect(win, [200,200,200], (40,20,160,90),0)
            editButton.color = [148,192,255]

            edit_UndoButton.updateLoc(42 ,22 , 156, 20 )
            edit_CutButton.updateLoc(42 ,44 , 156, 20 )
            edit_CopyButton.updateLoc(42 ,66 , 156, 20 )
            edit_PasteButton.updateLoc(42 ,88 , 156, 20 )

            edit_UndoButton.draw(win)
            edit_CutButton.draw(win)
            edit_CopyButton.draw(win)
            edit_PasteButton.draw(win)

            if event.type == pygame.MOUSEMOTION:
                if edit_UndoButton.isOver(pos):
                    edit_UndoButton.draw(win, highLight = [0,120,225])
                if edit_CutButton.isOver(pos):
                    edit_CutButton.draw(win, highLight = [0,120,225])
                if edit_CopyButton.isOver(pos):
                    edit_CopyButton.draw(win, highLight = [0,120,225])
                if edit_PasteButton.isOver(pos):
                    edit_PasteButton.draw(win, highLight = [0,120,225])
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if edit_UndoButton.isOver(pos):
                    print("Undo")
                if edit_CutButton.isOver(pos):
                    print("Cut")
                if edit_CopyButton.isOver(pos):
                    print("Copy")
                if edit_PasteButton.isOver(pos):
                    print("Paste")
                    

            
        else:
            editButton.color = white
        if mainMenuTopIndex == 2:
            pygame.draw.rect(win, [200,200,200], (80,20,160,90),0)
            toolsButton.color = [148,192,255]

            tools_TestButton.updateLoc(82 ,22 , 156, 20 )
            tools_RenderButton.updateLoc(82 ,44 , 156, 20 )
            tools_AddBackgroundButton.updateLoc(82 ,66 , 156, 20 )
            tools_ConnectButton.updateLoc(82 ,88 , 156, 20 )

            tools_TestButton.draw(win)
            tools_RenderButton.draw(win)
            tools_AddBackgroundButton.draw(win)
            tools_ConnectButton.draw(win)

            if event.type == pygame.MOUSEMOTION:
                if tools_TestButton.isOver(pos):
                    tools_TestButton.draw(win, highLight = [0,120,225])
                if tools_RenderButton.isOver(pos):
                    tools_RenderButton.draw(win, highLight = [0,120,225])
                if tools_AddBackgroundButton.isOver(pos):
                    tools_AddBackgroundButton.draw(win, highLight = [0,120,225])
                if tools_ConnectButton.isOver(pos):
                    tools_ConnectButton.draw(win, highLight = [0,120,225])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if tools_TestButton.isOver(pos):
                    print("Test")
                if tools_RenderButton.isOver(pos):
                    print("Render")
                if tools_AddBackgroundButton.isOver(pos):
                    print("Add Background")
                    layoutScreenDef.backGroundImage = pygame.image.load(easygui.fileopenbox())
                if tools_ConnectButton.isOver(pos):
                    print("Connect")

            
        else:
            toolsButton.color = white
        if mainMenuTopIndex == 3:
            pygame.draw.rect(win, [200,200,200], (120,20,160,90),0)
            viewButton.color = [148,192,255]

            view_FullScreenButton.updateLoc(122 ,22 , 156, 20 )
            view_WindowScreenButton.updateLoc(122 ,44 , 156, 20 )
            view_ZoomInButton.updateLoc(122 ,66 , 156, 20 )
            view_ZoomOutButton.updateLoc(122 ,88 , 156, 20 )

            view_FullScreenButton.draw(win)
            view_WindowScreenButton.draw(win)
            view_ZoomInButton.draw(win)
            view_ZoomOutButton.draw(win)

            if event.type == pygame.MOUSEMOTION:
                if view_FullScreenButton.isOver(pos):
                    view_FullScreenButton.draw(win, highLight = [0,120,225])
                if view_WindowScreenButton.isOver(pos):
                    view_WindowScreenButton.draw(win, highLight = [0,120,225])
                if view_ZoomInButton.isOver(pos):
                    view_ZoomInButton.draw(win, highLight = [0,120,225])
                if view_ZoomOutButton.isOver(pos):
                    view_ZoomOutButton.draw(win, highLight = [0,120,225])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if view_FullScreenButton.isOver(pos):
                    fullscreen = True
                    win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                if view_WindowScreenButton.isOver(pos):
                    fullscreen = False
                    win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
                if view_ZoomInButton.isOver(pos):
                    print("Zoom In")
                if view_ZoomOutButton.isOver(pos):
                    print("Zoom Out")


            
        else:
            viewButton.color = white
        if mainMenuTopIndex == 4:
            pygame.draw.rect(win, [200,200,200], (160,20,160,134),0)
            audioButton.color = [148,192,255]

            audio_FullSpeedButton.updateLoc(162 ,22 , 156, 20 )
            audio_HalfSpeedButton.updateLoc(162 ,44 , 156, 20 )
            audio_OneHalfSpeedButton.updateLoc(162 ,66 , 156, 20 )
            audio_TwoSpeedButton.updateLoc(162 ,88 , 156, 20 )
            audio_ThreeSpeedButton.updateLoc(162 ,110 , 156, 20 )
            audio_FourSpeedButton.updateLoc(162 ,132 , 156, 20 )

            audio_FullSpeedButton.draw(win)
            audio_HalfSpeedButton.draw(win)
            audio_OneHalfSpeedButton.draw(win)
            audio_TwoSpeedButton.draw(win)
            audio_ThreeSpeedButton.draw(win)
            audio_FourSpeedButton.draw(win)

            if event.type == pygame.MOUSEMOTION:
                if audio_FullSpeedButton.isOver(pos):
                    audio_FullSpeedButton.draw(win, highLight = [0,120,225])
                if audio_HalfSpeedButton.isOver(pos):
                    audio_HalfSpeedButton.draw(win, highLight = [0,120,225])
                if audio_OneHalfSpeedButton.isOver(pos):
                    audio_OneHalfSpeedButton.draw(win, highLight = [0,120,225])
                if audio_TwoSpeedButton.isOver(pos):
                    audio_TwoSpeedButton.draw(win, highLight = [0,120,225])
                if audio_ThreeSpeedButton.isOver(pos):
                    audio_ThreeSpeedButton.draw(win, highLight = [0,120,225])
                if audio_FourSpeedButton.isOver(pos):
                    audio_FourSpeedButton.draw(win, highLight = [0,120,225])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if audio_FullSpeedButton.isOver(pos):
                    print("Full Speed")
                if audio_HalfSpeedButton.isOver(pos):
                    print("1/2 Speed")
                if audio_OneHalfSpeedButton.isOver(pos):
                    print("1.5x Speed")
                if audio_TwoSpeedButton.isOver(pos):
                    print("2x Speed")
                if audio_ThreeSpeedButton.isOver(pos):
                    print("3x Speed")
                if audio_FourSpeedButton.isOver(pos):
                    print("4x Speed")
                    
        else:
            audioButton.color = white

            
    else:
        mouseScreenOverride = False
        fileButton.color = white
        editButton.color = white
        toolsButton.color = white
        viewButton.color = white
        audioButton.color = white



    if menuLastCheckOveride == -1:
        mainMenuTopIndex = -1
        menuLastCheckOveride = 0
        


        
    clock.tick(60)
    pygame.display.update()

    

