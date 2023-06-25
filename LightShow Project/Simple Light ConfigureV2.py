import pygame
import sys
import os
import time
import SerialCsvTest as PixelWrite
import ReadWriteDef as NumUpdate
import PixelEffects


pygame.init()

monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
win = pygame.display.set_mode((750, 750), pygame.RESIZABLE)
screen_w = pygame.display.Info().current_w
screen_h = pygame.display.Info().current_h


#-------Define Screen Colors-------#
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


###-------------Premade Modes------------###
twinkleLightButton = Button((darkGrey), 20, white,  'Twinkle')
testMode2 = Button((darkGrey), 15, white,  'Police Split')


ColorSelected = [100,100,100]
ColorSelectedNum = 0
SelectedLightNum = 0
PixelSelectedNum = [0,0]

TypedKeyPad = []


selectedLightValue_OnBar = [0,0] # [selectedValue, changeY]

MAXLIGHTNUM = 80
 
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
        
    ColorSelectR.updateLoc(10 , 335 , 75, 30 )
    ColorSelectR.text = str(ColorSelected[0])
    ColorSelectG.updateLoc(95 , 335 , 75, 30 )
    ColorSelectG.text = str(ColorSelected[1])
    ColorSelectB.updateLoc(180 , 335 , 75, 30 )
    ColorSelectB.text = str(ColorSelected[2])

    twinkleLightButton.updateLoc(10 , 400 , 80, 80 )
    testMode2.updateLoc(95 , 400 , 80, 80 )
    
    
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


    ColorSelectR.draw(win, ())
    ColorSelectG.draw(win, ())
    ColorSelectB.draw(win, ())


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

    if event.type == pygame.MOUSEBUTTONUP:
        selectedLightValue_OnBar = [0,0] # [selectedValue, changeY]

    x = 0
    while x<1:
        PixelWrite.sendPixel("000",
                        str(NumUpdate.updateDigitsNumber(x,3)),
                        str(NumUpdate.updateDigitsNumber(ColorSelected[1],3)),
                        str(NumUpdate.updateDigitsNumber(ColorSelected[2],3)))
        PixelWrite.sendPixel('999','999','999','999')
        x=x+1


    pygame.display.update()


