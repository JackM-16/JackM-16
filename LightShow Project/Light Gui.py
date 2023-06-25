import pygame
import sys
import os
import time
import LightGuiDef
import AudioPlotDef
#import SerialTrackless

pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h

#define colors here
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
lightGrey2 = (150,150,150)
lightGrey = (100,100,100)
darkGrey = (50,50,50)

#background/title
win.fill((225,0,0))  # Fills the screen with what ever color

pygame.display.set_caption("NAVIGATOR")#caption


#define ALL classes here:
class Button():
    def __init__ (self, color, text_height, textColor, text = ''):
        self.color = color
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.text_height = text_height
        self.textColor = textColor
        self.text = text

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height) 
    def draw(self,win,outline = None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-4,self.y-4,self.width+8,self.height+8),0)

        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.text_height)
            text = font.render(self.text, 1, (self.textColor))
            win.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))

    def shadow(self,win):
        pygame.draw.rect(win, (lightGrey), (self.x+4,self.y-4,self.width,self.height+4),0)
        self.draw(win, ())

                            
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#define other variables here
clock = pygame.time.Clock()
startScreen = True
fullscreen = False

currentScreen = "LAYOUT"
x = 0
testDict = {2.5: [1, ['Pixel', '001', '255', '255', '255']], 3.0: [2, ['Pixel', '001', '000', '000', '000'], ['Pixel', '050', '000', '000', '000']], 3.5: [1, ['Pixel', '002', '255', '000', '255']], 4.0: [2, ['Pixel', '015', '255', '255', '255'], ['Pixel', '016', '255', '255', '255']], 4.75: [1, ['Pixel', '015', '000', '000', '000']], 5.0: [1, ['Pixel', '002', '000', '000', '000']], 6.0: [3, ['Pixel', '010', '255', '000', '000'], ['Pixel', '012', '200', '255', '255'], ['Pixel', '013', '000', '100', '020']], 7.5: [5, ['Pixel', '010', '255', '000', '000'], ['Pixel', '000', '255', '000', '000'], ['Pixel', '047', '255', '000', '000'], ['Pixel', '054', '200', '255', '255'], ['Pixel', '056', '000', '255', '255']], .5:[2,['Pixel', '012', '255', '12', '200'],['Pixel', '045', '255', '45', '154']],10: [15, ['Pixel', '054', '255', '000', '000'], ['Pixel', '100', '255', '000', '000'], ['Pixel', '101', '255', '000', '000'], ['Pixel', '102', '200', '255', '255'], ['Pixel', '103', '000', '255', '255'],['Pixel', '104', '255', '000', '000'], ['Pixel', '105', '255', '000', '000'], ['Pixel', '106', '255', '000', '000'], ['Pixel', '107', '200', '255', '255'], ['Pixel', '108', '000', '255', '255'],['Pixel', '109', '255', '000', '000'], ['Pixel', '110', '255', '000', '000'], ['Pixel', '111', '255', '000', '000'], ['Pixel', '112', '200', '255', '255'], ['Pixel', '113', '000', '255', '255']]}

timeRepeat = 0
then = time.time()

testLight = LightGuiDef.lightLine((200,200,200), (25,350),((screen_w/5 * 4) - 30,500), 48)
joinLight = LightGuiDef.lightLine((200,200,200), (25,350),((screen_w/5 * 4) - 30,500), 24)

## testConnector = LightGuiDef.connector(500,500)
## testCirlceConnector = LightGuiDef.connector(450,450)

screenRect = Button((lightGrey), 40, white,  '')
startButton = Button((black), 50, white,  'CLICK TO START')

designButton = Button((darkGrey), 25, white,  'LAYOUT')
sequenceButton = Button((darkGrey), 25, white,  'SEQUENCE')
renderButton = Button((darkGrey), 25, white,  'RENDER')

addLineButton = Button((darkGrey), 25, white,  'ADD LINE')
addCircleButton = Button((darkGrey), 25, white,  'ADD CIRCLE')
addConnectorButton = Button((darkGrey), 25, white,  'ADD CONNECTOR')
addBackGroundButton = Button((darkGrey), 25, white,  'ADD BACKGROUND')

playSimulationButton = Button((darkGrey), 25, white,  'PLAY RENDER')

All_Layout_Shapes_Draw = []
All_Layout_Connector_Draw = []

lightShowArray  = LightGuiDef.cubeArray(1,20,10,350)

audioTestPlot = AudioPlotDef.audioWave('C:/Users/jtmti/Downloads/y2mate.com - GRAVES INTO GARDENS  ELEVATION WORSHIP LYRIC VIDEO.wav', 10, 45)

scatterTestPlot = AudioPlotDef.showGraph(testDict, 10, 350)

moveFarLeftButton = Button((darkGrey), 25, white,  'Move Left')
moveLittleLeftButton = Button((darkGrey), 25, white,  'Move .01 Left')
moveLittleRightButton = Button((darkGrey), 25, white,  'Move .01 Right')
moveFarRightButton = Button((darkGrey), 25, white,  'Move Right')

addAudioButton = Button((darkGrey), 25, white,  'ADD AUDIO')
addAudio3Button = Button((darkGrey), 25, white,  'ADD AUDIO3')
addAudio4Button = Button((darkGrey), 25, white,  'ADD AUDIO4')

addItemButton = Button((darkGrey), 25, white,  'ADD ITEM')
editItemButton = Button((darkGrey), 25, white,  'EDIT')

objectSelectionButton = Button((darkGrey), 27, white, 'Single')
editObjectSelectionButton = Button((darkGrey), 27, white, 'Edit')
leftMoveButton = Button((darkGrey), 27, white, 'Left')
rightMoveButton = Button((darkGrey), 27, white, 'Right')

lightNum_TextBox = Button((darkGrey), 25, white, '')

clickedItemArray = LightGuiDef.itemArray(500,500)
connectionsItemArray = LightGuiDef.lightConnectorArray(500,500)

clickedTime = 0

drawPictureRemove = False

while True:
    win.fill((lightGrey2))
    
    keys = pygame.key.get_pressed()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h

    #define button 
    startButton.updateLoc(screen_w/2 - (screen_w/6) , screen_h/2 - (screen_w/12) , screen_w/3 , screen_w/6)
    
    testLight.updateLoc((25,350),((screen_w/5 * 4) - 30,350))
    joinLight.updateLoc((int(screen_w/5 * 4) - 30,450),(25,550))
    #testLight.updateLoc((25,350),(25,100))
    
    designButton.updateLoc(5 , 5 , 100, 30 )
    sequenceButton.updateLoc(110 , 5 , 100, 30 )
    renderButton.updateLoc(215 , 5 , 100, 30 )
    
    addLineButton.updateLoc(5 , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 15, (screen_h/20))
    addCircleButton.updateLoc((screen_w/5) - 5, ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))
    addConnectorButton.updateLoc((screen_w/5 * 2) -10  , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))
    addBackGroundButton.updateLoc((screen_w/5  * 3) - 15  , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))

    addAudioButton.updateLoc(5 , ((screen_h/5 * 4)+10)+ 10 + (screen_h/20)  , (screen_w/5) - 30, (screen_h/20))
    addAudio3Button.updateLoc(5 , ((screen_h/5 * 4)+10)+ 15 + ((screen_h/20)*2)  , (screen_w/5) - 30, (screen_h/20))

    moveFarLeftButton.updateLoc(5 , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 15, (screen_h/20))
    moveLittleLeftButton.updateLoc((screen_w/5) - 5, ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))
    moveLittleRightButton.updateLoc((screen_w/5 * 2) -10  , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))
    moveFarRightButton.updateLoc((screen_w/5  * 3) - 15  , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 10, (screen_h/20))
    
    screenRect.updateLoc(5 , 40 , (screen_w/5 * 4) - 30 , (screen_h/5 * 4) - 30)
    playSimulationButton.updateLoc(5 , ((screen_h/5 * 4)+10)+ 5  , (screen_w/5) - 30, (screen_h/20))

    addItemButton.updateLoc((screen_w/5 * 4) - 20 , 5 , 100, 30)
    editItemButton.updateLoc((screen_w/5 * 4) + 85 , 5 , 100, 30)

    objectSelectionButton.updateLoc((screen_w/5 * 4) - 20 , 5 , 90, 30)
    editObjectSelectionButton.updateLoc((screen_w/5 * 4) + 75 , 5 , 90, 30)
    leftMoveButton.updateLoc((screen_w/5 * 4) + 170, 5 , 90, 30)
    rightMoveButton.updateLoc((screen_w/5 * 4) + 265 , 5 , 90, 30)

    lightNum_TextBox.updateLoc((screen_w/5 * 4) - 20 , screen_h/2 , screen_w - ((screen_w/5 * 4) - 30) - 15, 30)

    audioTestPlot.updateLocation(10, 45)
    scatterTestPlot.updateLocation(10, ((screen_h/5 * 4) - 30)/2 + 40, testDict)

    clickedItemArray.updateLocation((screen_w/5 * 4) - 20,40)
    connectionsItemArray.updateLocation((screen_w/5 * 4) - 20,40)
    
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

    
    screenRect.draw(win, ())
    designButton.draw(win, ())
    sequenceButton.draw(win, ())
    renderButton.draw(win, ())
                
    if currentScreen == "LAYOUT":
        if drawPictureRemove == True:
            picture2 = pygame.image.load("C:/Users/jtmti/Downloads/IMG_0403.jpg")
            #picture = pygame.transform.rotate(picture2, -90)
            picture = pygame.transform.scale(   picture2, (int((screen_w/5 * 4) - 30), int((screen_h/5 * 4) - 30))    )
            rect = picture.get_rect()
            rect = rect.move((5, 40))
            win.blit(picture, rect)
        pygame.draw.rect(win, (100,0,100), (400,200,400,400),0)
        
        selectedLightLineList = connectionsItemArray.returnClickedItems()
        
        for i in range(len(All_Layout_Shapes_Draw)):
            if objectSelectionButton.text == "Single":
                if i in selectedLightLineList:
                    All_Layout_Shapes_Draw[i].selected = True
                else:
                    All_Layout_Shapes_Draw[i].selected = False
            All_Layout_Shapes_Draw[i].draw(win,screen_w,screen_h)
        
        for i in range(len(All_Layout_Connector_Draw)):
            if objectSelectionButton.text != "Single":
                if i in selectedLightLineList:
                    All_Layout_Connector_Draw[i].selected(True)
                else:
                    All_Layout_Connector_Draw[i].selected(False)
            All_Layout_Connector_Draw[i].draw(win,screen_w,screen_h)
        
        designButton.shadow(win)
        addLineButton.draw(win)
        addCircleButton.draw(win)
        addConnectorButton.draw(win)
        addBackGroundButton.draw(win)
        objectSelectionButton.draw(win)
        editObjectSelectionButton.draw(win)
        leftMoveButton.draw(win)
        rightMoveButton.draw(win)
        lightNum_TextBox.draw(win)
        
        if objectSelectionButton.text == "Single":
            connectionsList = All_Layout_Shapes_Draw
            connectionsObject = None
        else:
            connectionsList = All_Layout_Connector_Draw
            connectionsObject = None
                    
        connectionsItemArray.draw(win,screen_w - ((screen_w/5 * 4) - 30) - 15 , screen_h/2, connectionsObject, connectionsList)

        #Buttons only in this screen
        if event.type == pygame.MOUSEMOTION:
            connectionsItemArray.hoverChangeSelected(pos, win)
            if addLineButton.isOver(pos):
                addLineButton.draw(win, (white))
            else:
                addLineButton.draw(win, ())
            if addCircleButton.isOver(pos):
                addCircleButton.draw(win, (white))
            else:
                addCircleButton.draw(win, ())
            if addConnectorButton.isOver(pos):
                addConnectorButton.draw(win, (white))
            else:
                addConnectorButton.draw(win, ())
            if addBackGroundButton.isOver(pos):
                addBackGroundButton.draw(win, (white))
            else:
                addBackGroundButton.draw(win, ())
            if objectSelectionButton.isOver(pos):
                objectSelectionButton.draw(win, (white))
            else:
                objectSelectionButton.draw(win, ())
            if editObjectSelectionButton.isOver(pos):
                editObjectSelectionButton.draw(win, (white))
            else:
                editObjectSelectionButton.draw(win, ())
            if leftMoveButton.isOver(pos):
                leftMoveButton.draw(win, (white))
            else:
                leftMoveButton.draw(win, ())
            if rightMoveButton.isOver(pos):
                rightMoveButton.draw(win, (white))
            else:
                rightMoveButton.draw(win, ())

        if event.type == pygame.MOUSEBUTTONDOWN:
            connectionsItemArray.clickScroll(pos)
            connectionsItemArray.clickItems(pos)
            connectionsItemArray.clickChangeSelected(pos)
            
            if addLineButton.isOver(pos):
                LightGuiDef.addLightLine(win, screen_w, screen_h,All_Layout_Shapes_Draw, lightNum_TextBox)
                pygame.time.wait(100)
            if addCircleButton.isOver(pos):
                LightGuiDef.addLightCirlce(win, screen_w, screen_h,All_Layout_Shapes_Draw)
                pygame.time.wait(100)
            if addConnectorButton.isOver(pos):
                newObjects = LightGuiDef.ConnectorGUI(All_Layout_Shapes_Draw)
                testConnector5 = LightGuiDef.connector(500,500, newObjects)
                All_Layout_Connector_Draw.append(testConnector5)
                pygame.time.wait(100)
            if addBackGroundButton.isOver(pos):
                drawPictureRemove = True
                pygame.time.wait(100)

            if objectSelectionButton.isOver(pos):
                if objectSelectionButton.text == "Single":
                    objectSelectionButton.text = "Connector"
                    objectSelectionButton.text_height = 22
                else:
                    objectSelectionButton.text = "Single"
                    objectSelectionButton.text_height = 27
                    
                pygame.time.wait(100)
            if editObjectSelectionButton.isOver(pos):
                pygame.time.wait(100)
            if leftMoveButton.isOver(pos):
                pygame.time.wait(100)
            if rightMoveButton.isOver(pos):
                fullLightLocationTouching = []
                for i in range(len(All_Layout_Shapes_Draw)):
                    fullLightLocation = (All_Layout_Shapes_Draw[i].getLocationList(screen_w,screen_h))
                    fullLightLocationTouching.append(LightGuiDef.inBoxLight(fullLightLocation, 400, 200, 400, 400))
                print(fullLightLocationTouching)
                pygame.time.wait(100)

            if lightNum_TextBox.isOver(pos):
                pygame.time.wait(100)
##                keysInPressed = LightGuiDef.textBox(win, lightNum_TextBox)
##                finalPressKeys = ''
##                for i in range(len(keysInPressed)):
##                    if keysInPressed[i].isdigit():
##                        finalPressKeys+=keysInPressed[i]
##                print(finalPressKeys)
        
    if currentScreen == "SEQUENCE":
        sequenceButton.shadow(win)
        addAudioButton.draw(win)
        addAudio3Button.draw(win)
        
        moveFarLeftButton.draw(win)
        moveLittleLeftButton.draw(win)
        moveLittleRightButton.draw(win)
        moveFarRightButton.draw(win)

        addItemButton.draw(win)
        editItemButton.draw(win)
        
        audioTestPlot.draw(win, (screen_w/5 * 4) - 40, ((screen_h/5 * 4) - 30)/2 - 10)
        scatterTestPlot.draw(win,(screen_w/5 * 4) - 40, ((screen_h/5 * 4) - 30)/2 - 10)
        audioTestPlot.drawLocationLine(win)
        scatterTestPlot.drawLocationLine(win) 
        clickedItemArray.draw(win,screen_w - ((screen_w/5 * 4) - 30) - 15 , screen_h, clickedTime, testDict)

        clickedTime = scatterTestPlot.getGraphNumber()
        
        if event.type == pygame.MOUSEMOTION:
            clickedItemArray.hoverChangeSelected(pos, win)
            if addAudioButton.isOver(pos):
                addAudioButton.draw(win, (white))
            else:
                addAudioButton.draw(win, ())

            if moveFarLeftButton.isOver(pos):
                moveFarLeftButton.draw(win, (white))
            else:
                moveFarLeftButton.draw(win, ())

            if moveLittleLeftButton.isOver(pos):
                moveLittleLeftButton.draw(win, (white))
            else:
                moveLittleLeftButton.draw(win, ())

            if moveLittleRightButton.isOver(pos):
                moveLittleRightButton.draw(win, (white))
            else:
                moveLittleRightButton.draw(win, ())

            if moveFarRightButton.isOver(pos):
                moveFarRightButton.draw(win, (white))
            else:
                moveFarRightButton.draw(win, ())
                
            if editItemButton.isOver(pos):
                editItemButton.draw(win, (white))
            else:
                editItemButton.draw(win, ())

            if addItemButton.isOver(pos):
                addItemButton.draw(win, (white))
            else:
                addItemButton.draw(win, ())

        if event.type == pygame.MOUSEBUTTONDOWN:
            clickedItemArray.clickScroll(pos)
            clickedItemArray.clickItems(pos)
            clickedItemArray.clickChangeSelected(pos)
            
            if pos[1] >= 40 and pos[1] <= (screen_h/5 * 4):
                audioTestPlot.click(pos,win,(screen_w/5 * 4) - 40)
                scatterTestPlot.click(pos,win,(screen_w/5 * 4) - 40)
            
            if addAudioButton.isOver(pos):
                Filename = AudioPlotDef.addFile()
                audioTestPlot.updateFile(Filename)
                
            if editItemButton.isOver(pos):
                clickedItemArray.editItems()
                scatterTestPlot.updateList(testDict)
                scatterTestPlot.draw(win,(screen_w/5 * 4) - 40, ((screen_h/5 * 4) - 30)/2 - 10, byPass = True)

            if addItemButton.isOver(pos):
               lightNumberListPassToAddList = LightGuiDef.formatLightsForAddArray(All_Layout_Shapes_Draw, All_Layout_Connector_Draw)
               clickedItemArray.addItem(lightNumberListPassToAddList)
               scatterTestPlot.updateList(testDict)
               scatterTestPlot.draw(win,(screen_w/5 * 4) - 40, ((screen_h/5 * 4) - 30)/2 - 10, byPass = True)

            if moveFarLeftButton.isOver(pos):
                audioTestPlot.StartTimeline = ((audioTestPlot.StartTimeline[0] - 1), audioTestPlot.StartTimeline[1])
                scatterTestPlot.StartTimeline = ((scatterTestPlot.StartTimeline[0] - 1), scatterTestPlot.StartTimeline[1])
                audioTestPlot.lastLength = audioTestPlot.lastLength +1
                scatterTestPlot.lastLength = scatterTestPlot.lastLength +1
                scatterTestPlot.changeGraphNumber(0, (screen_w/5 * 4) - 40)
                audioTestPlot.changeGraphNumber(0, (screen_w/5 * 4) - 40)
                
            if moveLittleLeftButton.isOver(pos):
                scatterTestPlot.changeGraphNumber(- .01, (screen_w/5 * 4) - 40)
                audioTestPlot.changeGraphNumber(- .01, (screen_w/5 * 4) - 40)
                
            if moveLittleRightButton.isOver(pos):
                scatterTestPlot.changeGraphNumber(.01,(screen_w/5 * 4) - 40)
                audioTestPlot.changeGraphNumber(.01,(screen_w/5 * 4) - 40)
                
            if moveFarRightButton.isOver(pos):
                audioTestPlot.StartTimeline = ((audioTestPlot.StartTimeline[0] + 1), audioTestPlot.StartTimeline[1])
                scatterTestPlot.StartTimeline = ((scatterTestPlot.StartTimeline[0] + 1), scatterTestPlot.StartTimeline[1])
                audioTestPlot.lastLength = audioTestPlot.lastLength +1
                scatterTestPlot.lastLength = scatterTestPlot.lastLength +1
                scatterTestPlot.changeGraphNumber(0, (screen_w/5 * 4) - 40)
                audioTestPlot.changeGraphNumber(0, (screen_w/5 * 4) - 40)


    if currentScreen == "RENDER":
        for i in range(len(All_Layout_Shapes_Draw)):
            All_Layout_Shapes_Draw[i].draw(win,screen_w,screen_h)
        for i in range(len(All_Layout_Connector_Draw)):
            All_Layout_Connector_Draw[i].draw(win,screen_w,screen_h)
            
##        testLight.draw(win)
##        joinLight.draw(win)
##        testConnector.draw(win, ())
##        renderButton.shadow(win)
##        playSimulationButton.draw(win, ())
##        testCircle.draw(win)
##        testCircle2.draw(win)
##        
##        #Buttons only in this screen
##        if event.type == pygame.MOUSEMOTION:
##            if playSimulationButton.isOver(pos):
##                playSimulationButton.draw(win, (white))
##            else:
##                playSimulationButton.draw(win, ())
##
##        if event.type == pygame.MOUSEBUTTONDOWN:
##            if playSimulationButton.isOver(pos):
##                then = time.time()
##                testHolder = [testLight,joinLight]
##                circleHolder = [testCircle,testCircle2]
##                testConnector.updateLightObjects(testHolder, win)
##                testCirlceConnector.updateLightObjects(circleHolder,win)
##                pygame.time.wait(100)
##
##        now = time.time() #Time after it finished
##        timerCount = round(now-then, 2)
##
##        if timerCount in testDict:
##            
##            itemNumber = testDict[timerCount]
##            print(timerCount)
##            x4 = 1
##            i = 0
##            while (i < itemNumber[timeRepeat]):
##                i = i + 1
##                pinNumber = itemNumber[x4][1]
##                R = itemNumber[x4][2]
##                G = itemNumber[x4][3]
##                B = itemNumber[x4][4]
##                
##                testConnector.connect(win,int(R),int(G),int(B),int(pinNumber))
##                testCirlceConnector.connect(win,int(R),int(G),int(B),int(pinNumber))
##                #testLight.lightColor(win, int(R),int(G),int(B),int(pinNumber))
##                
##                x4 = 1 + x4
                
    #Buttons on all the screens
    if event.type == pygame.MOUSEMOTION:
        if designButton.isOver(pos):
            designButton.draw(win, (white))
        else:
            designButton.draw(win, ())
        if sequenceButton.isOver(pos):
            sequenceButton.draw(win, (white))
        else:
            sequenceButton.draw(win, ())
        if renderButton.isOver(pos):
            renderButton.draw(win, (white))
        else:
            renderButton.draw(win, ())

    if event.type == pygame.MOUSEBUTTONDOWN:
        if designButton.isOver(pos):
            currentScreen = "LAYOUT"
            pygame.time.wait(250)
        else:
            designButton.draw(win, ())
        if sequenceButton.isOver(pos):
            currentScreen = "SEQUENCE"
            pygame.time.wait(250)
        else:
            sequenceButton.draw(win, ())
        if renderButton.isOver(pos):
            currentScreen = "RENDER"
            pygame.time.wait(250)
        else:
            renderButton.draw(win, ())
    
    pygame.display.update()
    

