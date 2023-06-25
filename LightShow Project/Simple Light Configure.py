import pygame
import sys
import os
import time
import threading
#import SerialTrackless
import SerialCsvTest as PixelWrite
import ReadWriteDef as NumUpdate
import PixelEffects


pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h

LightModeThread = " "

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
            #font = pygame.font.SysFont('comicsans', self.text_height)
            font = pygame.font.SysFont('arial', self.text_height)
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

def addToTotal(value, listname):
    if len(listname) < 5:
        listname.append(int(value))
def getTotalValue(value):
    Finalvalue = 0
    for x in range(len(value)):
        Finalvalue = (Finalvalue *10)+value[x]
    return(Finalvalue)

def RGBUpdate(value, index,lightColorList):
    Finalvalue = 0
    for x in range(len(value)):
        Finalvalue = (Finalvalue *10)+value[x]
    if Finalvalue > 255 :
        Finalvalue = 255
    if Finalvalue < 0:
        Finalvalue = 0
    lightColorList[index] = Finalvalue

def arrowPressed(value, selctedList):
    maxValue = 2
    if selctedList + value < 0:
        return(maxValue)
    elif selctedList + value > maxValue:
        return(0)
    else:
        return(selctedList+value)

def ASWDPressed(valuex,valuey, selctedList):
    maxValuex = 0
    maxValuey = 4
    if selctedList[0] + valuex < 0:
        selctedList[0] = maxValuex
    elif selctedList[0] + valuex  > maxValuex:
        selctedList[0] = 0
    else:
        selctedList[0] = selctedList[0] + valuex
    if selctedList[1] + valuey < 0:
        selctedList[1] = maxValuey
    elif selctedList[1] + valuey  > maxValuey:
        selctedList[1] = 0
    else:
        selctedList[1] = selctedList[1] + valuey

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self,):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        run = True
        while run == True:
            print("running")
            if LightModeThread == " ":
                print("")
            if LightModeThread == "twinkle":
                #PixelEffects.snowSparkle(45)
                PixelEffects.twinkle(80)
##                time.sleep(1.5)
                
            if LightModeThread == "policeSplit":
                PixelEffects.policeSplit(80)
                
            if LightModeThread == "candyCane":
                PixelEffects.candyCane(80)

            if LightModeThread == "stop":
                run = False

    
        
#background/title
win.fill((225,0,0))  # Fills the screen with what ever color

pygame.display.set_caption("Simple Light Config")#caption

#-------Define Variables-------#
clock = pygame.time.Clock()
fullscreen = False

#-------Define Buttons-------#
KeyPadButton0 = Button((darkGrey), 60, white,  '0')
KeyPadButton1 = Button((darkGrey), 60, white,  '1')
KeyPadButton2 = Button((darkGrey), 60, white,  '2')
KeyPadButton3 = Button((darkGrey), 60, white,  '3')
KeyPadButton4 = Button((darkGrey), 60, white,  '4')
KeyPadButton5 = Button((darkGrey), 60, white,  '5')
KeyPadButton6 = Button((darkGrey), 60, white,  '6')
KeyPadButton7 = Button((darkGrey), 60, white,  '7')
KeyPadButton8 = Button((darkGrey), 60, white,  '8')
KeyPadButton9 = Button((darkGrey), 60, white,  '9')
EnterKeyPadButton = Button((darkGrey), 35, white,  'ENTER')
LeftKeyPadButton = Button((darkGrey), 60, white,  '<')
RightKeyPadButton = Button((darkGrey), 60, white,  '>')
UpKeyPadButton = Button((darkGrey), 20, white,  'Up')
DownKeyPadButton = Button((darkGrey), 20, white,  'Down')
KeyPadTotalButton = Button((darkGrey), 60, white,  '100')
KeyPadClearButton = Button((darkGrey), 40, white,  'x')

ColorBackground1 = Button((lightGrey), 30, white,'')
ColorBackground2 = Button((lightGrey), 30, white,'')
ColorBackground3 = Button((lightGrey), 30, white,'')
ColorSelectR = Button((darkGrey), 30, white,  '255')
ColorSelectG = Button((darkGrey), 30, white,  '25')
ColorSelectB = Button((darkGrey), 30, white,  '100')


SelectedLightsButton = Button((darkGrey), 40, white,  '10000')
MaxLightsButton = Button((darkGrey), 40, white,  '10000')
SingleLightsButton = Button((darkGrey), 20, white,  'ONE')
AllLightsButton = Button((darkGrey), 20, white,  'ALL')
EvenLightsButton = Button((darkGrey), 20, white,  'EVEN')
OddLightsButton = Button((darkGrey), 20, white,  'ODD')


###-------------Premade Modes------------###
twinkleLightButton = Button((darkGrey), 20, white,  'Twinkle')
testMode2 = Button((darkGrey), 15, white,  'Police Split')
testMode3 = Button((darkGrey), 15, white,  'Candy Cane')
testMode4 = Button((darkGrey), 20, white,  'Test4')
testMode5 = Button((darkGrey), 20, white,  'Test5')
testMode6 = Button((darkGrey), 20, white,  'Test6')
testMode7 = Button((darkGrey), 20, white,  'Test7')
testMode8 = Button((darkGrey), 20, white,  'Test8')


ColorSelected = [255,25,100]
ColorSelectedNum = 0
SelectedLightNum = 0
PixelSelectedNum = [0,0]

TypedKeyPad = []

LightModeThreadRun = ThreadingExample()

selectedLightValue_OnBar = [0,0] # [selectedValue, changeY]

MAXLIGHTNUM = 80


PixelWrite.sendPixel('048','255','255','255')
PixelWrite.sendPixel('999','999','999','999')
PixelWrite.sendPixel('048','255','255','255')
PixelWrite.sendPixel('999','999','999','999')
 
while True:
    win.fill((lightGrey2))
    
    keys = pygame.key.get_pressed()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    
    #---Color---#
    pygame.draw.rect(win, ColorSelected, (10,5,245,55),0)
    #---Highlight Color Background---#
    if ColorSelectedNum == 0:
        pygame.draw.rect(win, white, (5,65,85,265),0)
    if ColorSelectedNum == 1:
        pygame.draw.rect(win, white, (90,65,85,265),0)
    if ColorSelectedNum == 2:
        pygame.draw.rect(win, white, (175,65,85,265),0)
    #---Color Background---#
    ColorBackground1.updateLoc(10,70,75,255 )
    ColorBackground2.updateLoc(95,70,75,255 )
    ColorBackground3.updateLoc(180,70,75,255 )

    ColorBackground1.draw(win, ())
    ColorBackground2.draw(win, ())
    ColorBackground3.draw(win, ())
    #---Color Slider---#    
    redValueRect = pygame.Rect(10,70,75,255 )
    greenValueRect = pygame.Rect(95,70,75,255 )
    blueValueRect = pygame.Rect(180,70,75,255 )


    pos = pygame.mouse.get_pos()
    if selectedLightValue_OnBar[0] == 1: # [selectedValue, changeY]
        RGBUpdate([255-(pos[1] - 70)], 0,ColorSelected)
    if selectedLightValue_OnBar[0] == 2: # [selectedValue, changeY]
        RGBUpdate([255-(pos[1] - 70)], 1,ColorSelected)
    if selectedLightValue_OnBar[0] == 3: # [selectedValue, changeY]
        RGBUpdate([255-(pos[1] - 70)], 2,ColorSelected)
    
    
    pygame.draw.rect(win, (200,200,200), (10,70+(255-ColorSelected[0]),75,ColorSelected[0]),0)
    pygame.draw.rect(win, (200,200,200), (95,70+(255-ColorSelected[1]),75,ColorSelected[1]),0)
    pygame.draw.rect(win, (200,200,200), (180,70+(255-ColorSelected[2]),75,ColorSelected[2]),0)


    KeyPadButton7.updateLoc(270 , 70 , 60, 60 )
    KeyPadButton8.updateLoc(335 , 70 , 60, 60 )
    KeyPadButton9.updateLoc(400 , 70 , 60, 60 )
    KeyPadButton4.updateLoc(270 , 135 , 60, 60 )
    KeyPadButton5.updateLoc(335 , 135 , 60, 60 )
    KeyPadButton6.updateLoc(400 , 135 , 60, 60 )
    KeyPadButton1.updateLoc(270 , 200 , 60, 60 )
    KeyPadButton2.updateLoc(335 , 200 , 60, 60 )
    KeyPadButton3.updateLoc(400 , 200 , 60, 60 )
    KeyPadButton0.updateLoc(270 , 265 , 60, 60 )
    EnterKeyPadButton.updateLoc(335 , 265 , 125, 60 )
    LeftKeyPadButton.updateLoc(270 , 330 , 60, 60 )
    RightKeyPadButton.updateLoc(400 , 330 , 60, 60 )
    UpKeyPadButton.updateLoc(335 , 330 , 60, 27 )
    DownKeyPadButton.updateLoc(335 , 362 , 60, 28 )
    KeyPadTotalButton.updateLoc(270 , 5 , 155, 60 )
    KeyPadTotalButton.text = ''.join(str(e) for e in TypedKeyPad)
    KeyPadClearButton.updateLoc(430 , 5 , 30, 60 )
        
    ColorSelectR.updateLoc(10 , 335 , 75, 30 )
    ColorSelectR.text = str(ColorSelected[0])
    ColorSelectG.updateLoc(95 , 335 , 75, 30 )
    ColorSelectG.text = str(ColorSelected[1])
    ColorSelectB.updateLoc(180 , 335 , 75, 30 )
    ColorSelectB.text = str(ColorSelected[2])

    SelectedLightsButton.updateLoc(470 , 5 , 125, 60 )
    SelectedLightsButton.text = str(SelectedLightNum)
    MaxLightsButton.updateLoc(600 , 5 , 125, 60 )
    
    SingleLightsButton.updateLoc(470 , 70 , 60, 60 )
    AllLightsButton.updateLoc(470 , 135 , 60, 60 )
    EvenLightsButton.updateLoc(470 , 200 , 60, 60 )
    OddLightsButton.updateLoc(470 , 265 , 60, 60 )

    twinkleLightButton.updateLoc(10 , 400 , 80, 80 )
    testMode2.updateLoc(95 , 400 , 80, 80 )
    testMode3.updateLoc(180 , 400 , 80, 80 )
    testMode4.updateLoc(265 , 400 , 80, 80 )
    testMode5.updateLoc(350 , 400 , 80, 80 )
    testMode6.updateLoc(435 , 400 , 80, 80 )
    testMode7.updateLoc(520 , 400 , 80, 80 )
    testMode8.updateLoc(605 , 400 , 80, 80 )
    

    
    

    
    #-------Get Mouse and Keys-------# 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("Scroll up")
            if event.button == 4:
                print("Scroll down")
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

        if keys[pygame.K_f]:
            fullscreen = not fullscreen
            if fullscreen:
                win = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
            else:
                win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)

        if keys[pygame.K_BACKSPACE] or keys[pygame.K_DELETE]:
            TypedKeyPad = []
        if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
            if ColorSelectedNum == 0:
                RGBUpdate(TypedKeyPad, 0,ColorSelected)
            if ColorSelectedNum == 1:
                RGBUpdate(TypedKeyPad, 1,ColorSelected)
            if ColorSelectedNum == 2:
                RGBUpdate(TypedKeyPad, 2,ColorSelected)


                
            
        if keys[pygame.K_0] or keys[pygame.K_KP0]:
            addToTotal(0, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_1] or keys[pygame.K_KP1]:
            addToTotal(1, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_2] or keys[pygame.K_KP2]:
            addToTotal(2, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_3] or keys[pygame.K_KP3]:
            addToTotal(3, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_4] or keys[pygame.K_KP4]:
            addToTotal(4, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_5] or keys[pygame.K_KP5]:
            addToTotal(5, TypedKeyPad)
            pygame.time.wait(125)
        if keys[pygame.K_6] or keys[pygame.K_KP6]:
            addToTotal(6, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_7] or keys[pygame.K_KP7]:
            addToTotal(7, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_8] or keys[pygame.K_KP8]:
            addToTotal(8, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_9] or keys[pygame.K_KP9]:
            addToTotal(9, TypedKeyPad)
            pygame.time.wait(100)
        if keys[pygame.K_LEFT]:
            ColorSelectedNum = arrowPressed(-1, ColorSelectedNum)
        if keys[pygame.K_RIGHT]:
            ColorSelectedNum = arrowPressed(1, ColorSelectedNum)
        if keys[pygame.K_UP]:
            if ColorSelectedNum == 0:
                RGBUpdate([ColorSelected[0]+10], 0,ColorSelected)
            if ColorSelectedNum == 1:
                RGBUpdate([ColorSelected[1]+10], 1,ColorSelected)
            if ColorSelectedNum == 2:
                RGBUpdate([ColorSelected[2]+10], 2,ColorSelected)
        if keys[pygame.K_DOWN]:
            if ColorSelectedNum == 0:
                RGBUpdate([ColorSelected[0]-10], 0,ColorSelected)
            if ColorSelectedNum == 1:
                RGBUpdate([ColorSelected[1]-10], 1,ColorSelected)
            if ColorSelectedNum == 2:
                RGBUpdate([ColorSelected[2]-10], 2,ColorSelected)

        if keys[pygame.K_w]:
            ASWDPressed(0,-1, PixelSelectedNum)
        if keys[pygame.K_s]:
            ASWDPressed(0,1, PixelSelectedNum)
        if keys[pygame.K_e]:
            if PixelSelectedNum == [0,0]:
                SelectedLightNum = getTotalValue(TypedKeyPad)
            if PixelSelectedNum == [0,1]:
                SelectedLightNum = "ALL"
            if PixelSelectedNum == [0,2]:
                SelectedLightNum = "EVEN"
            if PixelSelectedNum == [0,3]:
                SelectedLightNum = "ODD"

                
        if keys[pygame.K_z]:
            if PixelSelectedNum == [0,0]:
                SelectedLightNum = SelectedLightNum-1
        if keys[pygame.K_x]:
            if PixelSelectedNum == [0,0]:
                SelectedLightNum = SelectedLightNum+1

        if keys[pygame.K_SPACE]:
            if PixelSelectedNum == [0,0]:
                PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(SelectedLightNum,3)),
                                     str(NumUpdate.updateDigitsNumber(ColorSelected[0],3)),
                                     str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                                     str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))
            if PixelSelectedNum == [0,1]:
                for x in range(MAXLIGHTNUM):
                    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),
                                         str(NumUpdate.updateDigitsNumber(ColorSelected[0],3)),
                                         str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                                         str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))
            if PixelSelectedNum == [0,2]:
                for x in range(MAXLIGHTNUM):
                    if x % 2 == 0:
                        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[0],3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))
            if PixelSelectedNum == [0,3]:
                for x in range(MAXLIGHTNUM):
                    if x % 2 != 0:
                        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[0],3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                                             str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))

    
    if PixelSelectedNum == [0,4]:
        LightModeThread = "twinkle"
    elif PixelSelectedNum == [1,4]:
        LightModeThread = "policeSplit"
    elif PixelSelectedNum == [2,4]:
        LightModeThread = "candyCane"
    else:
        LightModeThread = " "

    KeyPadButton0.draw(win, ())
    KeyPadButton1.draw(win, ())
    KeyPadButton2.draw(win, ())
    KeyPadButton3.draw(win, ())
    KeyPadButton4.draw(win, ())
    KeyPadButton5.draw(win, ())
    KeyPadButton6.draw(win, ())
    KeyPadButton7.draw(win, ())
    KeyPadButton8.draw(win, ())
    KeyPadButton9.draw(win, ())
    EnterKeyPadButton.draw(win, ())
    LeftKeyPadButton.draw(win, ())
    RightKeyPadButton.draw(win, ())
    UpKeyPadButton.draw(win, ())
    DownKeyPadButton.draw(win, ())
    KeyPadTotalButton.draw(win, ())
    KeyPadClearButton.draw(win, ())

    ColorSelectR.draw(win, ())
    ColorSelectG.draw(win, ())
    ColorSelectB.draw(win, ())

    SelectedLightsButton.draw(win, ())
    MaxLightsButton.draw(win, ())
    if PixelSelectedNum == [0,0]:
        SingleLightsButton.draw(win, (white))
    else:
        SingleLightsButton.draw(win, ())
    if PixelSelectedNum == [0,1]:
        AllLightsButton.draw(win, (white))
    else:
        AllLightsButton.draw(win, ())
    if PixelSelectedNum == [0,2]:
        EvenLightsButton.draw(win, (white))
    else:
        EvenLightsButton.draw(win, ())
    if PixelSelectedNum == [0,3]:
        OddLightsButton.draw(win, (white))
    else:
        OddLightsButton.draw(win, ())

    if PixelSelectedNum == [0,4]:
        twinkleLightButton.draw(win, (white))
    else:
        twinkleLightButton.draw(win, ())
        
    if PixelSelectedNum == [1,4]:
        testMode2.draw(win, (white))
    else:
        testMode2.draw(win, ())
        
    if PixelSelectedNum == [2,4]:
        testMode3.draw(win, (white))
    else:
        testMode3.draw(win, ())
        
    testMode4.draw(win, ())
    testMode5.draw(win, ())
    testMode6.draw(win, ())
    testMode7.draw(win, ())
    testMode8.draw(win, ())

    if event.type == pygame.MOUSEBUTTONDOWN:
        pos = pygame.mouse.get_pos()
        if redValueRect.collidepoint(pos):
            selectedLightValue_OnBar = [1, pos[1] - redValueRect.y ] # [selectedValue, changeY]
        if greenValueRect.collidepoint(pos):
            selectedLightValue_OnBar = [2, pos[1] - greenValueRect.y] # [selectedValue, changeY]
        if blueValueRect.collidepoint(pos):
            selectedLightValue_OnBar = [3, pos[1] - blueValueRect.y] # [selectedValue, changeY]


        
        if ColorBackground1.isOver(pos):
            ColorSelectedNum = 0
            pygame.time.wait(50)
        if ColorBackground2.isOver(pos):
            ColorSelectedNum = 1
            pygame.time.wait(50)
        if ColorBackground3.isOver(pos):
            ColorSelectedNum = 2
            pygame.time.wait(50)

        if KeyPadButton0.isOver(pos):
            addToTotal(0, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton1.isOver(pos):
            addToTotal(1, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton2.isOver(pos):
            addToTotal(2, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton3.isOver(pos):
            addToTotal(3, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton4.isOver(pos):
            addToTotal(4, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton5.isOver(pos):
            addToTotal(5, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton6.isOver(pos):
            addToTotal(6, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton7.isOver(pos):
            addToTotal(7, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton8.isOver(pos):
            addToTotal(8, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadButton9.isOver(pos):
            addToTotal(9, TypedKeyPad)
            pygame.time.wait(50)
        if KeyPadClearButton.isOver(pos):
            TypedKeyPad = []
            
        if SingleLightsButton.isOver(pos):
            PixelSelectedNum = [0,0]
            pygame.time.wait(50)
        if AllLightsButton.isOver(pos):
            PixelSelectedNum = [0,1]
            pygame.time.wait(50)
        if EvenLightsButton.isOver(pos):
            PixelSelectedNum = [0,2]
            pygame.time.wait(50)
        if OddLightsButton.isOver(pos):
            PixelSelectedNum = [0,3]
            pygame.time.wait(50)
        if twinkleLightButton.isOver(pos):
            PixelSelectedNum = [0,4]
            pygame.time.wait(50)
        if testMode2.isOver(pos):
            PixelSelectedNum = [1,4]
            pygame.time.wait(50)
        if testMode3.isOver(pos):
            PixelSelectedNum = [2,4]
            pygame.time.wait(50)

        if EnterKeyPadButton.isOver(pos):
            if ColorSelectedNum == 0:
                RGBUpdate(TypedKeyPad, 0,ColorSelected)
            if ColorSelectedNum == 1:
                RGBUpdate(TypedKeyPad, 1,ColorSelected)
            if ColorSelectedNum == 2:
                RGBUpdate(TypedKeyPad, 2,ColorSelected)

        if SelectedLightsButton.isOver(pos):
            if PixelSelectedNum == [0,0]:
                SelectedLightNum = getTotalValue(TypedKeyPad)
            if PixelSelectedNum == [0,1]:
                SelectedLightNum = "ALL"
            if PixelSelectedNum == [0,2]:
                SelectedLightNum = "EVEN"
            if PixelSelectedNum == [0,3]:
                SelectedLightNum = "ODD"
        if LeftKeyPadButton.isOver(pos):
            ColorSelectedNum = arrowPressed(-1, ColorSelectedNum)
            pygame.time.wait(100)
        if RightKeyPadButton.isOver(pos):
            ColorSelectedNum = arrowPressed(1, ColorSelectedNum)
            pygame.time.wait(100)

    if event.type == pygame.MOUSEBUTTONUP:
        selectedLightValue_OnBar = [0,0] # [selectedValue, changeY]

        
    if PixelSelectedNum[1] < 4 :
        PixelWrite.sendPixel("049",
                             str(NumUpdate.updateDigitsNumber(ColorSelected[0],3)),
                             str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                             str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))
        PixelWrite.sendPixel('999','999','999','999')




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

    

