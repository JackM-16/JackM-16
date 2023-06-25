import pygame
from pygame import mixer
import math
import AudioPlotDef
import time
from copy import copy 
import LightGUIEffects

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

mixer.init()

PixelDrawSize = 3

class globalVariables():
    def __init__ (self,):
        #-------Define Test Variables-------#
        self.myTestDict = {'0':'a','1':'b','2':'c','3':'d','4':'e','5':'f','6':'g' }
        ####{  'objectName' : [object_type, startposition, endposition, numlight]  }
        self.myTestDict = {'0':['','','','']}
        self.lightObjectList = []
        self.imageBackgroundLayout = []

globalVariablesObj = globalVariables()


###-------Define Object-Oriented-Classes-------###
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
        
    def draw(self,win,outline = None, highLight = None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-4,self.y-4,self.width+8,self.height+8),0)
        if highLight:
            pygame.draw.rect(win, highLight, (self.x,self.y,self.width,self.height),0)
        else:
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


COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
class InputBox():
    def __init__(self, x, y, w, h,textHeight, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.textHeight = textHeight
        FONT = pygame.font.SysFont('arial', self.textHeight)
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        FONT = pygame.font.SysFont('arial', self.textHeight)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self,x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class ImageButton():
    def __init__ (self, imageFile):
        self.picture = pygame.image.load(imageFile)
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        
    def draw(self,win,):
        #Call this method to draw the button on the screen
        rect = self.picture.get_rect()
        rect = rect.move((self.x, self.y))
        win.blit(self.picture, rect)
                            
    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class listBox():
    def __init__ (self,highlightColor, text_height, textColor):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.highlightColor = highlightColor
        self.text_height = text_height
        self.textColor = textColor
        self.listofObjects = []
        self.highlightedNum = -1
        self.startNum = 0
        self.isEditingSelected = False
        self.text = ''

    def updateLoc(self,x,y,width,height, updateList):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.listofObjects = updateList
        
    def draw(self,win):
        #Call this method to draw the button on the screen
        #pygame.draw.rect(win, (255,255,255), (self.x,self.y,self.width,self.height),0)
        if self.listofObjects != []:
            if type(self.listofObjects) == list:
                for x in range(self.startNum, len(self.listofObjects)):
                    font = pygame.font.SysFont('arial', self.text_height-2)
                    text = font.render(self.listofObjects[x], 1, (self.textColor))
                    if self.highlightedNum == x and self.y +5+((x-self.startNum)*self.text_height)+self.text_height <self.y+self.height:
                        pygame.draw.rect(win, self.highlightColor, (self.x, self.y +5+((x-self.startNum)*self.text_height),self.width,self.text_height),0)
                    if self.y +5+((x-self.startNum)*self.text_height)+self.text_height <self.y+self.height:
                        win.blit(text, (self.x+5, self.y +5+((x-self.startNum)*self.text_height)))
                        
            if type(self.listofObjects) == dict:
                dictValues = list(self.listofObjects.keys())
                for x in range(self.startNum, len(dictValues)):
                    if self.highlightedNum == x and self.y +5+((x-self.startNum)*self.text_height)+self.text_height <self.y+self.height:
                        pygame.draw.rect(win, self.highlightColor, (self.x, self.y +5+((x-self.startNum)*self.text_height),self.width,self.text_height),0)
                        if self.isEditingSelected == True:
                            pygame.draw.rect(win, (255,255,255), (self.x+(self.width/2)-2, self.y +2+5+((x-self.startNum)*self.text_height),self.width/2+1,self.text_height-4),0)

                    font = pygame.font.SysFont('arial', self.text_height-2)
                    text = font.render(dictValues[x], 1, (self.textColor))
                    text2 = font.render(self.listofObjects[dictValues[x]], 1, (self.textColor))
                    if self.isEditingSelected == True and self.highlightedNum == x :
                        text2 = font.render(self.text, 1, (self.textColor))
                    if self.y +5+((x-self.startNum)*self.text_height)+self.text_height <self.y+self.height:
                        win.blit(text, (self.x+5, self.y +5+((x-self.startNum)*self.text_height)))
                        win.blit(text2, (self.x+(self.width/2), self.y +5+((x-self.startNum)*self.text_height)))

                    

    def getSelected(self):
        if self.highlightedNum < len(self.listofObjects):
            return(self.highlightedNum, self.listofObjects)
        else:
            return(-1, self.listofObjects)

    def editActive(self):
        if self.isEditingSelected == False:
            self.isEditingSelected = True
            print("Edit Start")
        else:
            self.isEditingSelected = False
            print("Edit End")

    def clampStartNum(self, value, firstValue):
        maxValue = len(self.listofObjects)
        maxValue = maxValue - self.height//self.text_height
        if maxValue < 0:
            maxValue = 0
        if firstValue + value < 0:
            return(0)
        elif firstValue + value > maxValue:
            return(maxValue)
        else:
            return(firstValue+value)

    def confirmNewValuePressed(self):
        if self.isEditingSelected:
            returnText = str(self.text)
            self.text = ''
            self.isEditingSelected = False
            return(returnText, self.highlightedNum)
        else:
            return(False)

        
    def eventHandler(self, event):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.startNum = self.clampStartNum(-1, self.startNum)
                    if event.button == 5:
                        self.startNum = self.clampStartNum(1, self.startNum)
                    if event.button == 1:
                        mousey = pos[1]-self.y
                        if self.highlightedNum == self.startNum + mousey//self.text_height:
                            if self.isEditingSelected == True:
                                self.isEditingSelected = False
                            elif self.isEditingSelected == False:
                                self.highlightedNum = -1
                            pygame.time.wait(50)
                        else:
                            if self.y +5+((mousey//self.text_height)*self.text_height)+self.text_height <self.y+self.height:
                                self.highlightedNum = self.startNum + (mousey//self.text_height)
                            else:
                                self.highlightedNum = -1
                            pygame.time.wait(50)
                if event.type == pygame.KEYDOWN:
                    if self.isEditingSelected:
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            if event.key != pygame.K_TAB and event.key != pygame.K_RETURN:
                                self.text += event.unicode
                        # Re-render the text.
                        #self.txt_surface = FONT.render(self.text, True, self.color)

class lightLine():
    def __init__(self,):
        self.name = "Light Line"
        self.start = [0,0]
        self.end = [1,1]
        self.numLights = 10
        self.selected = False

    def updateLocMouse(self, pos, index, screen_w, screen_h):
        if index == 2 or index == 3:
            
            self.start = [  (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
        if index == 4 or index == 5:
            self.end = [  (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
            
    def getData(self,screen_w,screen_h):
        return ({"Name":str(self.name),
                "Num Lights":str(self.numLights),
                "Start X":str(  int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.start[0] * globalVariablesObj.imageBackgroundLayout[2])) ,
                "Start Y":str(  globalVariablesObj.imageBackgroundLayout[1]+ int(self.start[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),
                "End X":str(    int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.end[0] * globalVariablesObj.imageBackgroundLayout[2]) ),
                "End Y":str(    globalVariablesObj.imageBackgroundLayout[1]+ int(self.end[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),})

    def updateData(self, newvalue, index, screen_w, screen_h):
        if index==0:
            self.name = newvalue
        elif index==1:
            self.numLights = int(newvalue)
        elif index==2:
            self.start[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==3:
            self.start[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]
        elif index==4:
            self.end[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==5:
            self.end[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]

    def getType(self):
        return("Line")

    def draw(self,win,screen_w,screen_h,active=False, pixelSizeOverride = 0):
        drawStartPosition = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.start[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.start[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        drawEndPosition = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.end[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.end[1] * globalVariablesObj.imageBackgroundLayout[3])   )
        xDistance = drawEndPosition[0] - drawStartPosition[0]
        yDistance = drawEndPosition[1] - drawStartPosition[1]
        pygame.draw.line(win,(75,75,75),(drawStartPosition), (drawEndPosition), 1)

        move = drawStartPosition[0]
        ymove = drawStartPosition[1]

        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        for i in range (self.numLights):
            if active==True:
                pygame.draw.circle(win, (0,150,255),(int(move),int(ymove+.5)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(int(move),int(ymove+.5)),FinalPixelDraw)
            
            move = move + (xDistance/(self.numLights-1))
            ymove = ymove + (yDistance/(self.numLights-1))



class lightCircle():
    def __init__(self,):
        self.name = "Light Circle"
        self.middle = [.5,.5]
        self.edge = [.1,.1]
        self.numLights = 10
        self.selected = False

    def updateLocMouse(self, pos, index, screen_w, screen_h):
        if index == 2 or index == 3:
            diff = pos[1] - (globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * (globalVariablesObj.imageBackgroundLayout[3])))
            newEdgeY = globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * (globalVariablesObj.imageBackgroundLayout[3])) + diff
            
            self.middle = [ (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]   ]
            self.edge = [  self.middle[0], (int(newEdgeY) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
        if index == 4:
            self.edge = [  self.middle[0], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
            
    def getData(self,screen_w,screen_h):
        return ({"Name":str(self.name),
                "Num Lights":str(self.numLights),
                "Middle X":str(  int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2])) ,
                "Middle Y":str(  globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),
                "Radius":str(    globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),})

    def updateData(self, newvalue, index, screen_w, screen_h):
        if index==0:
            self.name = newvalue
        elif index==1:
            self.numLights = int(newvalue)
        elif index==2:
            self.middle[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==3:
            self.middle[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]
        elif index==4:
            self.edge[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]

    def getType(self):
        return("Circle")

    def draw(self,win,screen_w,screen_h,active=False, pixelSizeOverride = 0):

        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        drawMiddleLocation = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        pygame.draw.circle(win, (0,0,100),drawMiddleLocation,FinalPixelDraw)

        finalEndDraw = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        radiusMath = abs( math.sqrt(((finalEndDraw[0] - drawMiddleLocation[0])**2) + ((finalEndDraw[1] - drawMiddleLocation[1])**2)))
        PI = 3.141592653
        angle = 1.570796326

        for i in range (self.numLights):
            x = radiusMath * math.sin(angle) + drawMiddleLocation[0] 
            y = radiusMath * math.cos(angle) + drawMiddleLocation[1]
            
            if active==True:
                pygame.draw.circle(win, (0,150,255),(int(x),int(y)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(int(x),int(y)),FinalPixelDraw)
            
            (360/self.numLights)* (PI/180)
            angle = angle + (360/self.numLights)* (PI/180)



class lightArc():
    def __init__(self,):
        self.name = "Light Arc"
        self.middle = [.5,.5]
        self.edge = [.1,.1]
        self.numLights = 10
        self.selected = False

    def updateLocMouse(self, pos, index, screen_w, screen_h):
        if index == 2 or index == 3:
            diff = pos[1] - (globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * (globalVariablesObj.imageBackgroundLayout[3])))
            newEdgeY = globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * (globalVariablesObj.imageBackgroundLayout[3])) + diff
            
            self.middle = [ (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]   ]
            self.edge = [  self.middle[0], (int(newEdgeY) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
        if index == 4:
            self.edge = [  self.middle[0], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
            
    def getData(self,screen_w,screen_h):
       return ({"Name":str(self.name),
                "Num Lights":str(self.numLights),
                "Middle X":str(  int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2])) ,
                "Middle Y":str(  globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),
                "Radius":str(    globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),})

    def updateData(self, newvalue, index, screen_w, screen_h):
        if index==0:
            self.name = newvalue
        elif index==1:
            self.numLights = int(newvalue)
        elif index==2:
            self.middle[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==3:
            self.middle[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]
        elif index==4:
            self.edge[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]

    def getType(self):
        return("Arc")

    def draw(self,win,screen_w,screen_h,active=False, pixelSizeOverride = 0):
        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        drawMiddleLocation = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.middle[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        pygame.draw.circle(win, (0,0,100),drawMiddleLocation,FinalPixelDraw)

        finalEndDraw = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.middle[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.edge[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        radiusMath = abs( math.sqrt(((finalEndDraw[0] - drawMiddleLocation[0])**2) + ((finalEndDraw[1] - drawMiddleLocation[1])**2)))
        PI = 3.141592653
        angle = 1.570796326
        for i in range (self.numLights):
            x = radiusMath * math.sin(angle) + drawMiddleLocation[0] 
            y = radiusMath * math.cos(angle) + drawMiddleLocation[1]
            
            if active==True:
                pygame.draw.circle(win, (0,150,255),(int(x),int(y)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(int(x),int(y)),FinalPixelDraw)
            
            (180/self.numLights)* (PI/180)
            angle = angle + (180/(self.numLights-1))* (PI/180)


class lightMatrix():
    def __init__(self,):
        self.name = "Light Matrix"
        self.start = [0,0]
        self.end = [1,1]
        self.lightArray = [10,10]
        self.selected = False

    def updateLocMouse(self, pos, index, screen_w, screen_h):
        if index == 3 or index == 3:
            self.start = [  (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
        if index == 5 or index == 6:
            self.end = [  (int(pos[0]) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2], (int(pos[1]) - globalVariablesObj.imageBackgroundLayout[1]) / (globalVariablesObj.imageBackgroundLayout[3])     ]
            
    def getData(self,screen_w,screen_h):
        return ({"Name":str(self.name),
                "Num Lights X":str(self.lightArray[0]),
                "Num Lights Y":str(self.lightArray[1]),
                "Start X":str(  int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.start[0] * globalVariablesObj.imageBackgroundLayout[2])) ,
                "Start Y":str(  globalVariablesObj.imageBackgroundLayout[1]+ int(self.start[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),
                "End X":str(    int(globalVariablesObj.imageBackgroundLayout[0]) + int(self.end[0] * globalVariablesObj.imageBackgroundLayout[2]) ),
                "End Y":str(    globalVariablesObj.imageBackgroundLayout[1]+ int(self.end[1] * (globalVariablesObj.imageBackgroundLayout[3]))  ),})

    def updateData(self, newvalue, index, screen_w, screen_h):
        if index==0:
            self.name = newvalue
        elif index==1:
            self.lightArray[0] = int(newvalue)
        elif index==2:
            self.lightArray[1] = int(newvalue)
        elif index==3:
            self.start[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==4:
            self.start[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]
        elif index==5:
            self.end[0] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[0]) / globalVariablesObj.imageBackgroundLayout[2]
        elif index==6:
            self.end[1] = (int(newvalue) - globalVariablesObj.imageBackgroundLayout[1]) / globalVariablesObj.imageBackgroundLayout[3]

    def getType(self):
        return("Matrix")

    def draw(self,win,screen_w,screen_h,active=False, pixelSizeOverride = 0):
        TopLeft = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.start[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.start[1] * globalVariablesObj.imageBackgroundLayout[3])    )
        BottomRight = (   globalVariablesObj.imageBackgroundLayout[0] + int(self.end[0] * globalVariablesObj.imageBackgroundLayout[2]), globalVariablesObj.imageBackgroundLayout[1]+ int(self.end[1] * globalVariablesObj.imageBackgroundLayout[3])   )
        xDistance = BottomRight[0] - TopLeft[0]
        yDistance = BottomRight[1] - TopLeft[1]
        #pygame.draw.line(win,(75,75,75),(drawStartPosition), (drawEndPosition), 1)
        
        currentX = TopLeft[0]
        currentY = TopLeft[1]

        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        for i in range (self.lightArray[1]):
            pygame.draw.line(win,(75,75,75),(TopLeft[0],currentY), (TopLeft[0]+xDistance,currentY), 1)
            for j in range (self.lightArray[0]):
                if active==True:
                    pygame.draw.circle(win, (0,150,255),(int(currentX),int(currentY+.5)),FinalPixelDraw)
                else:
                    pygame.draw.circle(win, (150,150,150),(int(currentX),int(currentY+.5)),FinalPixelDraw)
            
                currentX = currentX + (xDistance/(self.lightArray[0]-1))
            currentX = TopLeft[0]
            currentY = currentY + (yDistance/(self.lightArray[1]-1))



class audioTimeInput():
    def __init__ (self, color, text_height, textColor, text = ''):
        self.color = color
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.text_height = text_height
        self.textColor = textColor
        self.text = ["2","00","00"]

        self.currentEdit = -1
        self.isEditingSelected = False

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        
    def draw(self,win,outline = None, highLight = None):
        #Call this method to draw the button on the screen
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            #font = pygame.font.SysFont('comicsans', self.text_height)
            font = pygame.font.SysFont('arial', self.text_height)
            text1 = font.render(str(self.text[0])+":", 1, (self.textColor))
            text2 = font.render(str(self.text[1])+":", 1, (self.textColor))
            text3 = font.render(str(self.text[2]), 1, (self.textColor))

            
            if self.currentEdit == 0:
                pygame.draw.rect(win, [200,200,200], (self.x,self.y,text1.get_width(),25),0)
            if self.currentEdit == 1:
                pygame.draw.rect(win, [200,200,200], (self.x+text1.get_width(),self.y,text2.get_width(),25),0)
            if self.currentEdit == 2:
                pygame.draw.rect(win, [200,200,200], (self.x+text1.get_width()+text2.get_width(),self.y,text3.get_width(),25),0)
                
            win.blit(text1, (self.x, self.y ))
            win.blit(text2, (self.x+text1.get_width(), self.y ))
            win.blit(text3, (self.x+text1.get_width()+text2.get_width(), self.y ))

    def confirmNewValuePressed(self):
        if self.isEditingSelected:
            returnText = self.text
            self.text = ["0","0","0"]
            self.isEditingSelected = False
            self.currentEdit = -1
            return(int(returnText[0])*60+int(returnText[1])+int(returnText[2])*.01)
        else:
            return(False)
        
    def updateTextValue(self, newText):
        self.text = list(newText.split(":"))

    def updateCurrentIndex(self, newValue):
        start = -1
        end = 2
        if newValue < start:
            newValue = end
        elif newValue > end:
            newValue = start
        return(newValue)
        
    def eventHandler(self, event):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.currentEdit = self.updateCurrentIndex(self.currentEdit + 1)
                        self.isEditingSelected = True
                        
                if event.type == pygame.KEYDOWN:
                    if self.isEditingSelected:
                        if event.key == pygame.K_BACKSPACE and self.currentEdit > -1:
                            self.text[self.currentEdit] = self.text[self.currentEdit][:-1]
                        elif event.key == pygame.K_TAB:
                            self.currentEdit = self.updateCurrentIndex(self.currentEdit + 1)
                            self.isEditingSelected = True
                        else:
                            if event.key != pygame.K_TAB and event.key != pygame.K_RETURN:
                                if self.currentEdit > -1:
                                    self.text[self.currentEdit] += event.unicode



class sequenceLayoutChart():
    def __init__ (self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.text_height = 22
        self.textColor = black
        self.listofObjects = []
        self.highlightedNum = -1
        self.startIndexOffset = 0
        self.tileHeight = 0

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        
    def draw(self,win,textList = None):
        pygame.draw.rect(win, [30,30,30], (self.x,self.y,self.width,self.height),0)
        #side rectangle for objects
        pygame.draw.rect(win, [150,150,150], (self.x,self.y,140,self.height),0)
        
        self.tileHeight = self.height/20
        font = pygame.font.SysFont('arial', int(self.tileHeight/2))
        for x in range(20):
            addText = ""
            if textList != None:
                try:
                    addText = textList[ x+self.startIndexOffset]
                except:
                    addText = ""

            
            #pygame.draw.rect(win, [150,150,150], (self.x,self.y+(tileHeight * x),140,tileHeight),0)
            if self.highlightedNum == x+self.startIndexOffset:
                pygame.draw.rect(win, [220,220,220], (self.x,self.y+(self.tileHeight * x),140,self.tileHeight),0)

            text1 = font.render(str(str(x+self.startIndexOffset) + " - " + str(addText)), 1, (self.textColor))
            win.blit(text1, (self.x+2, 2+self.y+(self.tileHeight * x) ))
            pygame.draw.line(win,black,(self.x,self.y+(self.tileHeight * x)), (self.x+140,self.y+(self.tileHeight * x)), 1)
            if (x+self.startIndexOffset) % 2 ==0:
                pygame.draw.rect(win, [55,55,55], (self.x+140,self.y+(self.tileHeight * x),self.width-140,self.tileHeight),0)
        

    def getSelected(self):
        if self.highlightedNum < len(self.listofObjects):
            return(self.highlightedNum, self.listofObjects)
        else:
            return(-1, self.listofObjects)


        
    def eventHandler(self, event):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        tempValue = [0, self.startIndexOffset -1]
                        tempValue.sort()
                        self.startIndexOffset = tempValue[1]
                    if event.button == 5:
                        self.startIndexOffset = self.startIndexOffset +1

                    if event.button == 1:
                        mousey = pos[1]-self.y
                        if self.highlightedNum == int(self.startIndexOffset + mousey//self.tileHeight):
                            self.highlightedNum = -1
                            pygame.time.wait(50)
                        else:
                            self.highlightedNum = int(self.startIndexOffset + mousey//self.tileHeight)
                            pygame.time.wait(50)


























                                    






class layoutScreen():
    def __init__ (self):
        self.ModelsButton = Button(white, 17, black,  'Models')

        self.screenSize = (100,100)

        #----------Model Type Button----------#
        self.LineModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Line.png")
        self.PolyModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Poly Line.png")
        self.CircleModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Circle.png")
        self.ArcModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Arc.png")
        self.CandyCaneModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Candy Canes.png")
        self.MatrixModelButtonImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Matrix.png")

        #-----Image Backgrounds-----#
        self.ModelsBackGround = Button(white, 1, black,  '')
        self.LightSettingsBackGround = Button(white, 1, black,  '')
        self.backGroundImage = None
        self.ImageBackGround = Button([200,200,200], 22, black,  'Image')
        #-----ListBox-----#
        self.ModelListBox = listBox(lightGrey2, 22, black)
        self.ModelDetailsListBox = listBox(lightGrey2, 22, black)


        self.input_box1 = InputBox(400, 400, 150, 50, 20)
        self.isEditObjectData = False

    def draw(self,win, screen_w, screen_h):
        self.screenSize = (screen_w,screen_h)
        globalVariablesObj.imageBackgroundLayout = [(screen_w/6)+10 ,160 , (screen_w/6)*5-15, screen_h-165]
        
        self.ModelsButton.updateLoc(10 ,125 , 60, 30 )
        self.ModelsBackGround.updateLoc(11 ,161 , (screen_w/6)-7, ((screen_h-160)/5)*2 -2)
        self.LightSettingsBackGround.updateLoc(11 ,160 + ((screen_h-160)/5)*2 +11 , (screen_w/6)-7, ((screen_h-160)/5)*3 -16)
        self.ImageBackGround.updateLoc((screen_w/6)+10 ,160 , (screen_w/6)*5-15, screen_h-165)

        #----------Model Type Button Updates----------#
        self.LineModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0],125 , 30, 30 )
        self.PolyModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+35 ,125 , 30, 30 )
        self.CircleModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+70 ,125 , 30, 30 )
        self.ArcModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+105 ,125 , 30, 30 )
        self.CandyCaneModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+140 ,125 , 30, 30 )
        self.MatrixModelButtonImage.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+175 ,125 , 30, 30 )

    
        self.ModelsButton.draw(win)
        
        #----------Model Type Button Draw----------#
        self.LineModelButtonImage.draw(win)
        self.PolyModelButtonImage.draw(win)
        self.CircleModelButtonImage.draw(win)
        self.ArcModelButtonImage.draw(win)
        self.CandyCaneModelButtonImage.draw(win)
        self.MatrixModelButtonImage.draw(win)

        #----------Image BackGrounds Draw----------#
        pygame.draw.rect(win, [0,0,0], (10 ,160 , (screen_w/6)-5, ((screen_h-160)/5)*2),0)###Black Border
        self.ModelsBackGround.draw(win)
        pygame.draw.rect(win, [0,0,0], (10 ,160 + ((screen_h-160)/5)*2 +10 , (screen_w/6)-5, ((screen_h-160)/5)*3 -14),0)###Black Border
        self.LightSettingsBackGround.draw(win)
        
        self.ImageBackGround.draw(win)

        if self.backGroundImage != None:
            picture = pygame.transform.scale(self.backGroundImage, ((screen_w/6)*5-15, screen_h-165))
            rect = picture.get_rect()
            rect = rect.move(((screen_w/6)+10 ,160))
            win.blit(picture, rect)

        #----------ListBox Update and Draw----------#
        tempLightObjectList = []
        for x in range(len(globalVariablesObj.lightObjectList)):
            tempLightObjectList.append(str(globalVariablesObj.lightObjectList[x].name))
        
        self.ModelListBox.updateLoc(11 ,160+22 , (screen_w/6)-7, ((screen_h-160)/5)*2 -22, tempLightObjectList)

        tempLightObjectSelectedDict = []
        if self.ModelListBox.getSelected()[0] != -1:
            tempLightObjectSelectedDict = globalVariablesObj.lightObjectList[self.ModelListBox.getSelected()[0]].getData(screen_w,screen_h)
        self.ModelDetailsListBox.updateLoc(11 ,160 + ((screen_h-160)/5)*2 +11 , (screen_w/6)-7, ((screen_h-160)/5)*3 -16, tempLightObjectSelectedDict)
        
        self.ModelListBox.draw(win)
        self.ModelDetailsListBox.draw(win)

        ######--------------Draw LightObjects--------------######
        if self.ModelListBox.getSelected()[0] > -1:
            tempObjectSlected = globalVariablesObj.lightObjectList[self.ModelListBox.getSelected()[0]]
        else:
            tempObjectSlected = None
        for obj in globalVariablesObj.lightObjectList:
            if obj == tempObjectSlected:
                obj.draw(win,screen_w,screen_h, active=True)
            else:
                obj.draw(win,screen_w,screen_h)

        ###-----Type Header for Models -----###
        font = pygame.font.SysFont('arial', 20)
        text = font.render("Model/Name", 1, black)
        win.blit(text, (15, 160))
####        text = font.render("|Name", 1, black)
####        win.blit(text, (((screen_w/3)-10-7)/2, 160))


##        if self.isEditObjectData == True:
##            #(11+(((screen_w/3)-17)/2), (5+160 + ((screen_h-160)/5)*2 +11) +5+((x-self.startNum)*22))
##            self.input_box1.update(11 ,5+160 + ((screen_h-160)/5)*2 +11 , (screen_w/3)-10-7, 24)
##            self.input_box1.update(11+(((screen_w/3)-17)/2), (160 + ((screen_h-160)/5)*2 +11) +5+((1-0)*20),11+(((screen_w/3)-17)/2), 24)
##            self.input_box1.draw(win)

    def updateLightObjectsFromListBox(index, newValue):
        print(newValue)
        tempObjectSlected = globalVariablesObj.lightObjectList[self.ModelListBox.getSelected()[0]]
        
    def eventHandler(self, event):
        self.ModelListBox.eventHandler(event)
        self.ModelDetailsListBox.eventHandler(event)
        self.input_box1.handle_event(event)


        keys = pygame.key.get_pressed()
        if keys[pygame.K_TAB]:
            self.ModelDetailsListBox.editActive()
        if keys[pygame.K_RETURN]:
            tempValue = self.ModelDetailsListBox.confirmNewValuePressed()
            if tempValue != False:
                lightObjectSelected = globalVariablesObj.lightObjectList[self.ModelListBox.getSelected()[0]]
                lightObjectSelected.updateData(tempValue[0], tempValue[1], self.screenSize[0], self.screenSize[1])
        #-----Deletes selected object from list by hitting delete key-----#
        if keys[pygame.K_DELETE]:
            selectedObject = self.ModelListBox.getSelected()[0]
            if selectedObject != -1:
                globalVariablesObj.lightObjectList.pop(selectedObject)
                time.sleep(.1)
                

        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.LineModelButtonImage.isOver(pos):
                globalVariablesObj.lightObjectList.append( lightLine() )
            if self.CircleModelButtonImage.isOver(pos):
                globalVariablesObj.lightObjectList.append( lightCircle() )
            if self.ArcModelButtonImage.isOver(pos):
                globalVariablesObj.lightObjectList.append( lightArc() )
            if self.MatrixModelButtonImage.isOver(pos):
                globalVariablesObj.lightObjectList.append( lightMatrix() )

            if self.ModelDetailsListBox.isEditingSelected == True and self.ModelDetailsListBox.getSelected()[0] != -1:
                lightObjectSelected = globalVariablesObj.lightObjectList[self.ModelListBox.getSelected()[0]]
                
                lightObjectSelected.updateLocMouse(pos, self.ModelDetailsListBox.getSelected()[0], self.screenSize[0], self.screenSize[1])




class sequenceScreen():
    def __init__ (self):
        self.screenSize = (100,100)

        mixer.music.load("C:/Users/jtmti/Downloads/Easy Beat.wav")
        self.musicMode = "stop"
        self.audioPlayTimeStart = 0
        self.audioPauseTime = 0
        
        #-----Image Backgrounds-----#
        self.sequenceBackGround = Button([200,200,200], 22, black,  'Sequence')
        self.modelPreview = Button([0,0,0], 22, white,  '')#Model Preview
        self.effectSetting = Button([255,255,255], 22, black,  'Effect Settings')
        self.housePreview = Button([0,0,0], 22, white,  '')#House Preview

        self.sequenceLayoutBar = sequenceLayoutChart()

        self.timeSelected = Button([150,150,150], 22, black,  'Time: 0:00:00')
        self.timeUpdateBox = audioTimeInput([150,150,150], 22, black,  '0:00:00')

        self.playPauseButton = Button([150,150,150], 22, black,  'Play/Pause')
        self.resetAudioButton = Button([150,150,150], 22, black,  'Reset')

        
        self.audioGraph = AudioPlotDef.audioWavePlot('C:/Users/jtmti/Downloads/Blinding Lights(1).wav')

    def draw(self,win, screen_w, screen_h):
        self.screenSize = (screen_w,screen_h)
        globalVariablesObj.imageBackgroundLayout = [(screen_w/6)+10 ,160 , (screen_w/6)*5-15, screen_h-165]
        
        self.sequenceBackGround.updateLoc((screen_w/6)+10 ,160 , (screen_w/6)*5-15, screen_h-165)

        pygame.draw.rect(win, [0,0,0], (5 ,160 , (screen_w/6), ((screen_h-160)/6)*2 -28 ),0)###Black Border
        self.modelPreview.updateLoc(6 ,161 , (screen_w/6)-2, ((screen_h-160)/6)*2 -30)
        
        pygame.draw.rect(win, [0,0,0], (5 ,160 + ((screen_h-160)/6)*2 - 21, (screen_w/6), ((screen_h-160)/6)*3 - 40-18),0)###Black Border
        self.effectSetting.updateLoc(6 ,160 + ((screen_h-160)/6)*2 - 20, (screen_w/6)-2, ((screen_h-160)/6)*3 - 40-20)
        
        pygame.draw.rect(win, [0,0,0], (5 ,160 + ((screen_h-160)/6)*2 -20 + ((screen_h-160)/6)*3 - 51 , (screen_w/6), ((screen_h-160)/6) +62),0)###Black Border
        self.housePreview.updateLoc(6 ,160 + ((screen_h-160)/6)*2 -20 + ((screen_h-160)/6)*3 - 50 , (screen_w/6)-2, ((screen_h-160)/6) +60)
        
        self.sequenceBackGround.draw(win)
        self.modelPreview.draw(win)
        self.effectSetting.draw(win)
        self.housePreview.draw(win)


        self.timeSelected.updateLoc((screen_w/6)+10 ,160 , 140, (screen_h-165)/14)
        self.timeUpdateBox.updateLoc((screen_w/6)+10 ,160 + (screen_h-165)/14 , 140, (screen_h-165)/14)

        self.sequenceLayoutBar.updateLoc((screen_w/6)+10 ,160 + (screen_h-165)/7, (screen_w/6)*5-15, (screen_h-165)/7*6)
        
        returnListNames = ["All Lights",]
        for obj in globalVariablesObj.lightObjectList:
            returnListNames.append(obj.name)
        self.sequenceLayoutBar.draw(win, textList = returnListNames)

        
        if self.musicMode == "play":
            self.audioGraph.lineDrawTime = (time.time() - self.audioPlayTimeStart) + self.audioPauseTime
            #self.audioGraph.lineDrawTime = (mixer.music.get_pos()/1000)+self.audioPauseTime
        self.timeSelected.text = self.audioGraph.getTimeSelected()
        self.timeSelected.draw(win)
        self.timeUpdateBox.draw(win)

        self.playPauseButton.updateLoc(globalVariablesObj.imageBackgroundLayout[0]+105,125 , 120, 30 )
        self.resetAudioButton.updateLoc(globalVariablesObj.imageBackgroundLayout[0],125 , 100, 30 )

        self.playPauseButton.draw(win)
        self.resetAudioButton.draw(win)

        self.audioGraph.updateLoc((screen_w/6)+10 + 140,160,(screen_w/6)*5-15 -140, (screen_h-165)/7)
        self.audioGraph.draw(win)

        #-----Draw selected light by itself in top left-----#
        if self.sequenceLayoutBar.highlightedNum > -1:
            selectNum = self.sequenceLayoutBar.highlightedNum
            globalVariablesObj.imageBackgroundLayout = [6 ,161 , (screen_w/6)-2, ((screen_h-160)/6)*2 -30]
            try:
                if selectNum-1 > -1:
                    selectLightNum = globalVariablesObj.lightObjectList[selectNum-1]
                    tempCopyofSelectLight = copy(selectLightNum)
                    if tempCopyofSelectLight.getType() == "Line" or "Matrix":
                        tempCopyofSelectLight.start = [.1,.1]
                        tempCopyofSelectLight.end = [.9,.9]
                    elif tempCopyofSelectLight.getType() == "Circle":
                        tempCopyofSelectLight.middle = [.5,.5]
                        tempCopyofSelectLight.edge = [.1,.1]
                    if tempCopyofSelectLight.getType() == "Arc":
                        tempCopyofSelectLight.middle = [.5,.65]
                        tempCopyofSelectLight.edge = [.1,.25]
                    tempCopyofSelectLight.draw(win,screen_w,screen_h, pixelSizeOverride=3)
            except:
                pass



        #-----Draw house preview only lights in bottom left corner-----#
        globalVariablesObj.imageBackgroundLayout = [6 ,160 + ((screen_h-160)/6)*2 -20 + ((screen_h-160)/6)*3 - 50 , (screen_w/6)-2, ((screen_h-160)/6) +60]
        for obj in globalVariablesObj.lightObjectList:
            obj.draw(win,screen_w,screen_h, pixelSizeOverride=1)
        

        
    def eventHandler(self, event):
        self.audioGraph.eventHandler(event)
        self.timeUpdateBox.eventHandler(event)
        self.sequenceLayoutBar.eventHandler(event)

        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playPauseButton.isOver(pos):
                self.playAudio()
            if self.resetAudioButton.isOver(pos):
                self.musicMode = "stop"
                self.playAudio()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            tempValue = self.timeUpdateBox.confirmNewValuePressed()
            if tempValue != False:
                print(tempValue)
                self.audioGraph.lineDrawTime = tempValue
                print(self.audioGraph.lineDrawTime)

        if keys[pygame.K_SPACE]:
            print(globalVariablesObj.lightObjectList)

    def playAudio(self):
        if self.musicMode == "stop":
            mixer.music.play()
            self.audioPauseTime = 0
            self.audioPlayTimeStart = time.time()
            self.musicMode = "play"
            
        elif self.musicMode == "play":
            mixer.music.pause()
            self.audioPauseTime = self.audioGraph.lineDrawTime
            self.musicMode = "pause"

        elif self.musicMode == "pause":
            mixer.music.unpause()
            self.audioPlayTimeStart = time.time()
            self.musicMode = "play"
            
            