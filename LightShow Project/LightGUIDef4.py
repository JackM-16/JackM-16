import pygame
import math
import LightPLTEffect4 as effect

class colors():
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

def textInput(event, currentValue):
    currentValue = str(currentValue)
    returnText = currentValue
    if event.key == pygame.K_BACKSPACE:
        returnText = currentValue[:-1]
    else:
        if event.key != pygame.K_TAB and event.key != pygame.K_RETURN:
            returnText = currentValue + event.unicode
    return(returnText)

def globalIsOver(pos,rect):
    if pos[0] > rect[0] and pos[0] < rect[0] + rect[2]:
        if pos[1] > rect[1] and pos[1] < rect[1] + rect[3]:
            return True
            
    return False

class globalVariables():
    lightObjectDisplayList = []

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
        self.over = False
        self.highlight = False

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        
    def draw(self,win,outline = None, highLight = None):
        #Call this method to draw the button on the screen
        if self.over==True :
            pygame.draw.rect(win, [255,255,255], (self.x-2,self.y-2,self.width+4,self.height+4),0)
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
        if highLight:
            pygame.draw.rect(win, highLight, (self.x,self.y,self.width,self.height),0)
        elif self.highlight:
            pygame.draw.rect(win, [0,120,225], (self.x,self.y,self.width,self.height),0)
        else:
            pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            #font = pygame.font.SysFont('comicsans', self.text_height)
            font = pygame.font.SysFont('arial', self.text_height)
            text = font.render(self.text, 1, (self.textColor))
            win.blit(text, (self.x + int(self.width/2 - text.get_width()/2), self.y + int(self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class ImageButton(Button):
    def __init__(self, imageFile):
        self.picture = pygame.image.load(imageFile)
        super().__init__([0,0,0,], 0, 0, '')
    def draw(self, win, overSized = False):
        super().draw(win)
        rect = self.picture.get_rect()
        rect = rect.move((self.x, self.y))
        if overSized == True:
            self.picture = pygame.transform.scale(self.picture, (self.width, self.height))
        win.blit(self.picture, rect)
    def reloadPic(self, imageFile):
        self.picture = pygame.image.load(imageFile)

class listBox():
    def __init__ (self, color, text_height, textColor):
        self.color = color
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.text_height = text_height
        self.textColor = textColor
        self.listOfObjects = []
        self.currentStart = 0
        self.selectedNum = -1
        self.highlightcolor = [150,150,150]
        self.hoverNum = -1
        self.hoverColor = [210,210,210]
        self.scrollable = False
        self.maxShown = 1
        self.isEditing = False
        

    def updateLoc(self,x,y,width,height, updateList):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

        self.listOfObjects = updateList
        if len(updateList) * self.text_height > self.height:
            self.scrollable = True
            self.maxShown = self.height//self.text_height - 1
        else:
            self.scrollable = False
        
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)

        if self.listOfObjects != []:
            if type(self.listOfObjects) == list:
                #draw scrollbar
                if self.scrollable == True:
                    scrollRatio = (self.height/((len(self.listOfObjects)+1) * self.text_height))
                    yscroll = self.y+2 + (self.currentStart*(self.text_height*scrollRatio))
                    pygame.draw.rect(win, [50,50,50], (self.x+self.width-10, yscroll ,8, scrollRatio*self.height -2),0)
                for x in range(self.currentStart, len(self.listOfObjects)):
                    yvalueRect = self.y +5+((x-self.currentStart)*self.text_height)
                    if (yvalueRect + self.text_height) < self.y + self.height:
                        if x == self.selectedNum:
                            pygame.draw.rect(win, self.highlightcolor, (self.x, yvalueRect,self.width-12,self.text_height),0)

                        font = pygame.font.SysFont('arial', self.text_height-2)
                        text = font.render(str(self.listOfObjects[x]), 1, (self.textColor))
                        win.blit(text, (self.x+5, yvalueRect))
                    else:
                        break

            if type(self.listOfObjects) == dict:
                #draw scrollbar
                dictValues = list(self.listOfObjects.keys())
                if self.scrollable == True:
                    scrollRatio = (self.height/((len(dictValues)+1) * self.text_height))
                    yscroll = self.y+2 + (self.currentStart*(self.text_height*scrollRatio))
                    pygame.draw.rect(win, [50,50,50], (self.x+self.width-10, yscroll ,8, scrollRatio*self.height -2),0)
                
                for x in range(self.currentStart, len(dictValues)):
                    yvalueRect = self.y +5+((x-self.currentStart)*self.text_height)
                    if (yvalueRect + self.text_height) < self.y + self.height:
                        if x == self.selectedNum:
                            pygame.draw.rect(win, self.highlightcolor, (self.x, yvalueRect,self.width-12,self.text_height),0)
                            if self.isEditing:
                                pygame.draw.rect(win, [200,200,200], (self.x + (self.width-12)//2, yvalueRect,(self.width-12)//2,self.text_height),0)

                        font = pygame.font.SysFont('arial', self.text_height-2)
                        text = font.render(str(dictValues[x]), 1, (self.textColor))
                        text2 = font.render(str(self.listOfObjects[dictValues[x]]), 1, (self.textColor))
                        win.blit(text, (self.x+5, yvalueRect))
                        win.blit(text2, (self.x+5 + (self.width/2), yvalueRect))
                    else:
                        break


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def hoverSelection(self, pos):
        if self.isOver(pos):
            calcValue = (pos[1]-self.y-3) // self.text_height
            if calcValue + self.currentStart < len(self.listOfObjects):
                self.hoverNum = calcValue + self.currentStart
            else:
                self.hoverNum = len(self.listOfObjects) -1


    def scrollWheel(self, valueChange):
        if self.scrollable == True:
            temp = self.currentStart + valueChange
            if temp < 0:
                self.currentStart = 0
            elif temp > len(self.listOfObjects)-self.maxShown-1:
                self.currentStart = len(self.listOfObjects) - self.maxShown -1
            else:
                self.currentStart = self.currentStart + valueChange





PixelDrawSize = 3

class lightLineOBJ():
    def __init__ (self,):
        self.name = "Light Line"
        self.start = [.1,.1]
        self.end = [.9,.9]
        self.numLights = 10
        self.selected = False
        self.isEditingValues = False
        self.listVariables = [self.name,self.numLights,self.start[0],self.start[1],self.end[0],self.end[1]]

    def getData(self,x,y,w,h,):
        if self.isEditingValues == True:
            return ( { "Name:":str(self.listVariables[0]),
            "Num Lights":str(self.listVariables[1]),
            "Start X":str(int(self.listVariables[2])),
            "Start Y":str(int(self.listVariables[3])),
            "End X":str(int(self.listVariables[4])),
            "End Y":str(int(self.listVariables[5])),
            } )
        else:
            self.listVariables = [self.name,self.numLights,int(self.start[0]*w),int(self.start[1]*h),int(self.end[0]*w),int(self.end[1]*h)]
            return ( { "Name:":str(self.name),
            "Num Lights":str(self.numLights),
            "Start X":str(int(self.start[0]*w)),
            "Start Y":str(int(self.start[1]*h)),
            "End X":str(int(self.end[0]*w)),
            "End Y":str(int(self.end[1]*h)),
            } )

    def updateSelected(self, selectedNum, changedValue,width, height):
        self.isEditingValues = True
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int(self.end[0]*width),int(self.end[1]*height)]
        if selectedNum > 1:
            if changedValue == "":
                self.listVariables[selectedNum] = int(0)
            else:
                self.listVariables[selectedNum] = int(changedValue)
        else:
            self.listVariables[selectedNum] = changedValue


    def confirmSelected(self, selectedNum, width, height):
        self.isEditingValues = False
        if selectedNum == 0:
            self.name = str(self.listVariables[selectedNum])
        elif selectedNum == 1:
            if int(self.listVariables[selectedNum]) < 2:
                self.numLights = 2
            else:
                self.numLights = int(self.listVariables[selectedNum])
        elif selectedNum == 2:
            self.start[0] = self.listVariables[selectedNum]/width
        elif selectedNum == 3:
            self.start[1] = self.listVariables[selectedNum]/height
        elif selectedNum == 4:
            self.end[0] = self.listVariables[selectedNum]/width
        elif selectedNum == 5:
            self.end[1] = self.listVariables[selectedNum]/height

    def updateByMouse(self, selectedNum,pos,width, height):
        updatedPos = (int(pos[0]-310),int(pos[1]-90))
        if selectedNum == 2 or selectedNum == 3:
            self.start[0] = updatedPos[0]/width
            self.start[1] = updatedPos[1]/height
        elif selectedNum == 4 or selectedNum == 5:
            self.end[0] = updatedPos[0]/width
            self.end[1] = updatedPos[1]/height
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int(self.end[0]*width),int(self.end[1]*height)]

    
            

    def draw(self,win,x ,y ,screen_w,screen_h, pixelSizeOverride = 0):
        drawStartPosition = [self.start[0]*screen_w , self.start[1]*screen_h]
        drawEndPosition = [self.end[0]*screen_w , self.end[1]*screen_h]
        xDistance = drawEndPosition[0] - drawStartPosition[0]
        yDistance = drawEndPosition[1] - drawStartPosition[1]
        pygame.draw.line(win,(75,75,75),(x + drawStartPosition[0], y + drawStartPosition[1]), (x + drawEndPosition[0], y + drawEndPosition[1]), 1)

        move = drawStartPosition[0]
        ymove = drawStartPosition[1]

        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        for i in range (self.numLights):
            if self.selected==True:
                pygame.draw.circle(win, (0,150,255),(x + int(move),y + int(ymove+.5)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(x + int(move),y + int(ymove+.5)),FinalPixelDraw)
            
            move = move + (xDistance/(self.numLights-1))
            ymove = ymove + (yDistance/(self.numLights-1))

class lightCircleOBJ():
    def __init__ (self,):
        self.name = "Light Circle"
        self.start = [.5,.5]
        self.end = [.55,.4]
        self.numLights = 10
        self.selected = False
        self.isEditingValues = False
        self.listVariables = [self.name,self.numLights,self.start[0],self.start[1],self.end[0]]


    def getData(self, x ,y ,screen_w,screen_h):
        if self.isEditingValues == True:
            return ( { "Name:":str(self.listVariables[0]),
            "Num Lights":str(self.listVariables[1]),
            "Middle X":str(int(self.listVariables[2])),
            "Middle Y":str(int(self.listVariables[3])),
            "Radius":str(int(self.listVariables[4])),
            } )
        else:
            self.listVariables = [self.name,self.numLights,int(self.start[0]*screen_w),int(self.start[1]*screen_h),int((abs(self.start[0]*screen_w - self.end[0]*screen_w)))]
            return ( { "Name:":str(self.name),
            "Num Lights":str(self.numLights),
            "Middle X":str(int(self.start[0]*screen_w)),
            "Middle Y":str(int(self.start[1]*screen_h)),
            "Radius":str(int((abs(self.start[0]*screen_w - self.end[0]*screen_w)))),
            } )
        
    def updateSelected(self, selectedNum, changedValue,width, height):
        self.isEditingValues = True
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int((abs(self.start[0]*width - self.end[0]*width)))]
        if selectedNum > 1:
            if changedValue == "":
                self.listVariables[selectedNum] = int(0)
            else:
                self.listVariables[selectedNum] = int(changedValue)
        else:
            self.listVariables[selectedNum] = changedValue

    def confirmSelected(self, selectedNum, width, height):
        self.isEditingValues = False
        if selectedNum == 0:
            self.name = str(self.listVariables[selectedNum])
        elif selectedNum == 1:
            if int(self.listVariables[selectedNum]) < 2:
                self.numLights = 2
            else:
                self.numLights = int(self.listVariables[selectedNum])
        elif selectedNum == 2:
            self.start[0] = self.listVariables[selectedNum]/width
        elif selectedNum == 3:
            self.start[1] = self.listVariables[selectedNum]/height
        elif selectedNum == 4:
            self.end[0] = (abs(self.start[0]*width + self.listVariables[selectedNum]))/width

    def updateByMouse(self, selectedNum,pos,width, height):
        updatedPos = (int(pos[0]-310),int(pos[1]-90))
        if selectedNum == 2 or selectedNum == 3:
            self.start[0] = updatedPos[0]/width
            self.start[1] = updatedPos[1]/height
        elif selectedNum == 4:
            self.end[0] = updatedPos[0]/width
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int((abs(self.start[0]*width - self.end[0]*width)))]


    def draw(self,win,x ,y ,screen_w,screen_h, pixelSizeOverride = 0):
        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        drawMiddleLocation = ( x+  self.start[0]*screen_w ,y+ self.start[1]*screen_h)
        pygame.draw.circle(win, (0,0,100),drawMiddleLocation,FinalPixelDraw)

        radiusMath = (abs(self.start[0]*screen_w - self.end[0]*screen_w))
        PI = 3.141592653
        angle = 1.570796326

        for i in range (self.numLights):
            x = radiusMath * math.sin(angle) + drawMiddleLocation[0] 
            y = radiusMath * math.cos(angle) + drawMiddleLocation[1]
            
            if self.selected==True:
                pygame.draw.circle(win, (0,150,255),(int(x),int(y)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(int(x),int(y)),FinalPixelDraw)
            
            (360/self.numLights)* (PI/180)
            angle = angle + (360/self.numLights)* (PI/180)

class lightArcOBJ():
    def __init__ (self,):
        self.name = "Light Arc"
        self.start = [.5,.5]
        self.end = [.25,.55]
        self.numLights = 10
        self.selected = False
        self.isEditingValues = False
        self.listVariables = [self.name,self.numLights,self.start[0],self.start[1],self.end[1]]

    def getData(self, x ,y ,screen_w,screen_h):
        if self.isEditingValues == True:
            return ( { "Name:":str(self.listVariables[0]),
            "Num Lights":str(self.listVariables[1]),
            "Middle X":str(int(self.listVariables[2])),
            "Middle Y":str(int(self.listVariables[3])),
            "Radius":str(int(self.listVariables[4])),
            } )
        else:
            self.listVariables = [self.name,self.numLights,int(self.start[0]*screen_w),int(self.start[1]*screen_h),int((abs(self.start[0]*screen_w - self.end[0]*screen_w)))]
            return ( { "Name:":str(self.name),
            "Num Lights":str(self.numLights),
            "Middle X":str(int(self.start[0]*screen_w)),
            "Middle Y":str(int(self.start[1]*screen_h)),
            "Radius":str(int((abs(self.start[0]*screen_w - self.end[0]*screen_w)))),
            } )
        
    def updateSelected(self, selectedNum, changedValue,width, height):
        self.isEditingValues = True
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int((abs(self.start[0]*width - self.end[0]*width)))]
        if selectedNum > 1:
            if changedValue == "":
                self.listVariables[selectedNum] = int(0)
            else:
                self.listVariables[selectedNum] = int(changedValue)
        else:
            self.listVariables[selectedNum] = changedValue

    def confirmSelected(self, selectedNum, width, height):
        self.isEditingValues = False
        if selectedNum == 0:
            self.name = str(self.listVariables[selectedNum])
        elif selectedNum == 1:
            if int(self.listVariables[selectedNum]) < 2:
                self.numLights = 2
            else:
                self.numLights = int(self.listVariables[selectedNum])
        elif selectedNum == 2:
            self.start[0] = self.listVariables[selectedNum]/width
        elif selectedNum == 3:
            self.start[1] = self.listVariables[selectedNum]/height
        elif selectedNum == 4:
            self.end[0] = (abs(self.start[0]*width + self.listVariables[selectedNum]))/width

    def updateByMouse(self, selectedNum,pos,width, height):
        updatedPos = (int(pos[0]-310),int(pos[1]-90))
        if selectedNum == 2 or selectedNum == 3:
            self.start[0] = updatedPos[0]/width
            self.start[1] = updatedPos[1]/height
        elif selectedNum == 4:
            self.end[0] = updatedPos[0]/width
        self.listVariables = [self.name,self.numLights,int(self.start[0]*width),int(self.start[1]*height),int((abs(self.start[0]*width - self.end[0]*width)))]


    def draw(self,win,x ,y ,screen_w,screen_h, pixelSizeOverride = 0):
        if pixelSizeOverride > 0 :
            FinalPixelDraw = pixelSizeOverride
        else:
            FinalPixelDraw = PixelDrawSize

        drawMiddleLocation = ( x+  self.start[0]*screen_w ,y+ self.start[1]*screen_h)
        pygame.draw.circle(win, (0,0,100),drawMiddleLocation,FinalPixelDraw)

        radiusMath = (abs(self.start[0]*screen_w - self.end[0]*screen_w))
        PI = 3.141592653
        angle = 1.570796326

        for i in range (self.numLights):
            x = radiusMath * math.sin(angle) + drawMiddleLocation[0] 
            y = radiusMath * math.cos(angle) + drawMiddleLocation[1]
            
            if self.selected==True:
                pygame.draw.circle(win, (0,150,255),(int(x),int(y)),FinalPixelDraw)
            else:
                pygame.draw.circle(win, (150,150,150),(int(x),int(y)),FinalPixelDraw)
            
            (180/self.numLights)* (PI/180)
            angle = angle + (180/(self.numLights-1))* (PI/180)


class layoutScreen():
    def __init__(self):
        self.modelTabButton = Button([150,150,150], 16, colors.black, "Model")
        self.mainModelListbox = listBox([175,175,175], 22, colors.black)
        self.settingsTabButton = Button([150,150,150], 16, colors.black, "Settings")
        self.settingsListbox = listBox([175,175,175], 22, colors.black)

        self.lineImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Line.png")
        self.polyLineImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Poly Line.png")
        self.circleImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Circle.png")
        self.arcImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Arc.png")
        self.matrixImage = ImageButton("C:/Users/jtmti/Documents/LightShow Project/Images/Matrix.png")

        self.windowDisplayValues = [1,1]
        self.isEditingSettings = False

    def activeRun(self, win, width, height):
        self.windowDisplayValues = [width-315, height-95]

        self.modelTabButton.updateLoc(5,60,70,25)
        currentLightList = []
        for obj in globalVariables.lightObjectDisplayList:
            currentLightList.append(obj.name)
        self.mainModelListbox.updateLoc(5, 90, 300, (height-90)/2 -5 - 25, currentLightList)
        self.settingsTabButton.updateLoc(5, 90 + (height-90)/2- 25 ,70,20)
        if self.mainModelListbox.selectedNum > -1:
            currentSelectedData = globalVariables.lightObjectDisplayList[self.mainModelListbox.selectedNum].getData(310, 90, width-315, (height-90)-5,)
        else:
            currentSelectedData = {}
        self.settingsListbox.updateLoc(5, 90 + (height-90)/2, 300, (height-90)/2 -5, currentSelectedData)

        self.lineImage.updateLoc(310,58,30,30)
        self.polyLineImage.updateLoc(345,58,30,30)
        self.circleImage.updateLoc(380,58,30,30)
        self.arcImage.updateLoc(415,58,30,30)
        self.matrixImage.updateLoc(450,58,30,30)

        self.modelTabButton.draw(win)
        self.mainModelListbox.draw(win)
        self.settingsTabButton.draw(win)
        self.settingsListbox.draw(win)

        self.lineImage.draw(win)
        self.polyLineImage.draw(win)
        self.circleImage.draw(win)
        self.arcImage.draw(win)
        self.matrixImage.draw(win)

        ##Draw backgroundScreen
        pygame.draw.rect(win, colors.black, (310, 90 ,width-315, (height-90)-5),0)

        for obj in globalVariables.lightObjectDisplayList:
            obj.draw(win, 310, 90, width-315, (height-90)-5, )

    def allEvent(self, event, pos):
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEMOTION:
            self.mainModelListbox.hoverSelection(pos)
            self.settingsListbox.hoverSelection(pos)

            self.lineImage.over = self.lineImage.isOver(pos)
            self.polyLineImage.over = self.polyLineImage.isOver(pos)
            self.circleImage.over = self.circleImage.isOver(pos)
            self.arcImage.over = self.arcImage.isOver(pos)
            self.matrixImage.over = self.matrixImage.isOver(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.mainModelListbox.isOver(pos):
                if event.button == 1:
                    self.mainModelListbox.selectedNum = self.mainModelListbox.hoverNum
                if event.button == 4:
                    self.mainModelListbox.scrollWheel(-1)
                if event.button == 5:
                    self.mainModelListbox.scrollWheel(1)

            if self.settingsListbox.isOver(pos):
                if event.button == 1:
                    self.settingsListbox.selectedNum = self.settingsListbox.hoverNum
                if event.button == 3:
                    self.isEditingSettings = not(self.isEditingSettings)
                    self.settingsListbox.selectedNum = self.settingsListbox.hoverNum
                    self.settingsListbox.isEditing = self.isEditingSettings
                if event.button == 4:
                    self.settingsListbox.scrollWheel(-1)
                if event.button == 5:
                    self.settingsListbox.scrollWheel(1)

            if self.lineImage.isOver(pos):
                if event.button == 1:
                    globalVariables.lightObjectDisplayList.append(lightLineOBJ())
            if self.circleImage.isOver(pos):
                if event.button == 1:
                    globalVariables.lightObjectDisplayList.append(lightCircleOBJ())
            if self.arcImage.isOver(pos):
                if event.button == 1:
                    globalVariables.lightObjectDisplayList.append(lightArcOBJ())
            
            if globalIsOver(pos,[310,90] + self.windowDisplayValues):
                if self.isEditingSettings:
                    if event.button == 1:
                        currentObj = globalVariables.lightObjectDisplayList[self.mainModelListbox.selectedNum]
                        currentObj.updateByMouse(self.settingsListbox.selectedNum,pos,self.windowDisplayValues[0],self.windowDisplayValues[1])

        if event.type == pygame.KEYDOWN:
            if self.isEditingSettings == True:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    self.isEditingSettings = False
                    self.settingsListbox.isEditing = self.isEditingSettings
                    currentObj = globalVariables.lightObjectDisplayList[self.mainModelListbox.selectedNum]
                    currentObj.confirmSelected(self.settingsListbox.selectedNum,self.windowDisplayValues[0], self.windowDisplayValues[1])
                else:
                    currentObj = globalVariables.lightObjectDisplayList[self.mainModelListbox.selectedNum]
                    currentObj.updateSelected(self.settingsListbox.selectedNum, textInput(event, currentObj.listVariables[self.settingsListbox.selectedNum]),self.windowDisplayValues[0], self.windowDisplayValues[1])
            if keys[pygame.K_TAB]:
                if self.settingsListbox.isOver(pos):
                    print(self.settingsListbox.selectedNum)


            



class sequenceScreen():
    def __init__(self):
        self.previewWindowButton = Button([0,0,0], 22, colors.white, "Preview")

        self.effectSettingsButton = Button([150,150,150], 14, colors.black, "Settings")
        self.effectSettingsListbox = listBox([175,175,175], 22, colors.black)
        self.effectColorButton = Button([150,150,150], 14, colors.black, "Colors")
        self.effectColorListbox = listBox([175,175,175], 22, colors.black)

        self.mainSequenceButton = Button([0,0,0], 22, colors.white, "Sequence")

        #"name of effect":[imageFilePath, name of effect in other program]
        sequenceEffectTypes = {"off":['C:/Users/jtmti/Documents/LightShow Project/Images/Effect_Icons/off.png', "offEffect"], "on":["C:/Users/jtmti/Documents/LightShow Project/Images/Effect_Icons/on.png", "onEffect"]}
        self.effectButtonList = {}
        listInteration = list(sequenceEffectTypes.keys())
        for x in range(len(listInteration)):
            currentObj = list(sequenceEffectTypes.values())[x]
            self.effectButtonList[ImageButton(currentObj[0])] = currentObj[1]

        self.isMouseDown = False

        self.testWavePlotter = effect.imagePlotter('C:/Users/jtmti/Downloads/Blinding Lights(1).wav', 'C:/Users/jtmti/Documents/LightShow Project/Images/waveFile.jpg')
        self.wavePlotButton = ImageButton('C:/Users/jtmti/Documents/LightShow Project/Images/waveFile.jpg')
        self.seqStartStop = [0,self.testWavePlotter.maxlength]
        self.waveStartTimeButon = Button([255,255,255], 14, colors.black, "0:00:00")
        self.waveEndTimeButon = Button([255,255,255], 14, colors.black, "0:00:00")
        self.waveLeftButton = Button([255,255,255], 14, colors.black, "|<")
        self.playPauseButton = Button([255,255,255], 14, colors.black, "Play")
        self.waveRightButton = Button([255,255,255], 14, colors.black, ">|")

    def activeRun(self, win, width, height):
        self.previewWindowButton.updateLoc(5,60, 335, 250)

        self.effectSettingsButton.updateLoc(5,315,70,20)
        self.effectSettingsListbox.updateLoc(5, 340, 335, (height-340)/2 -20, [0,1,2])
        self.effectColorButton.updateLoc(5,340 + (height-340)/2-15,70,20)
        self.effectColorListbox.updateLoc(5, 340 + (height-340)/2+10, 335, (height-340)/2 -15, [0,1,2])

        self.mainSequenceButton.updateLoc(345,95,(width-350), (height-95)-5 )

        self.previewWindowButton.draw(win)

        self.effectSettingsButton.draw(win)
        self.effectSettingsListbox.draw(win)
        self.effectColorButton.draw(win)
        self.effectColorListbox.draw(win)

        self.mainSequenceButton.draw(win)

        #Draws effectButtons from Dict
        keyList = list(self.effectButtonList.keys())
        for x in range(len(keyList)):
            keyList[x].updateLoc(345 + (35*x),60,30,30)
            keyList[x].draw(win, overSized = True)

        self.waveStartTimeButon.updateLoc(345,95,60, 30)
        self.waveStartTimeButon.text = str(effect.changeTimeType(self.seqStartStop[0]))
        self.waveEndTimeButon.updateLoc(width-65,95,60, 30)
        self.waveEndTimeButon.text = str(effect.changeTimeType(self.seqStartStop[1]))
        self.waveLeftButton.updateLoc(345+65,95,30, 30)
        self.playPauseButton.updateLoc(345+65+35,95,50, 30)
        self.waveRightButton.updateLoc(345+65+35+55,95,30, 30)
        self.wavePlotButton.updateLoc(345,95+30,(width-350), 100)

        self.waveStartTimeButon.draw(win)
        self.waveEndTimeButon.draw(win)
        self.waveLeftButton.draw(win)
        self.playPauseButton.draw(win)
        self.waveRightButton.draw(win)
        self.wavePlotButton.draw(win,)
        #####THis will load the plot image and put it a 100,100 starting from s=5 tp 10
        #self.testWavePlotter.updateGraph(5,10)
        ##seqPic = pygame.image.load('C:/Users/jtmti/Documents/LightShow Project/Images/waveFile.jpg')
        ##rect = seqPic.get_rect()
        ##rect = rect.move((100, 100))
        ##win.blit(seqPic, rect)

    def allEvent(self, event, pos):
        keys = pygame.key.get_pressed()
        if event.type == pygame.MOUSEMOTION:
            self.effectSettingsListbox.hoverSelection(pos)
            self.effectColorListbox.hoverSelection(pos)

            #Highlights effectButtons from Dict if Hovered
            keyList = list(self.effectButtonList.keys())
            for x in range(len(keyList)):
                keyList[x].over = keyList[x].isOver(pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.isMouseDown = True

            if self.wavePlotButton.isOver(pos):
                if event.button == 4:#Zoom in 
                    self.changeWaveEndZoom(-1)
                if event.button == 5:#Zoom out 
                    self.changeWaveEndZoom(1)

        if event.type == pygame.MOUSEBUTTONUP:
            self.isMouseDown = False

        if event.type == pygame.KEYDOWN:
            if self.wavePlotButton.isOver(pos):
                if keys[pygame.K_RIGHT]:
                    self.changeWaveStart(5)
                if keys[pygame.K_LEFT]:
                    self.changeWaveStart(-5)

        if event.type == pygame.WINDOWRESIZED:
            self.changeWaveEndZoom(event.dict['x'])

    def changeWaveEndZoom(self,changeValue):
        if self.seqStartStop[1] - self.seqStartStop[0] > 15:
            changeBy = 10
        if self.seqStartStop[1] - self.seqStartStop[0] > 8:
            changeBy = 5
        else:
            changeBy = 1
        if changeValue == -1:
            tempChange = self.seqStartStop[1] - changeBy
            if tempChange - self.seqStartStop[0] > changeBy:
                self.seqStartStop[1] = tempChange
        elif changeValue == 1: 
            self.seqStartStop[1] += changeBy
        else:
            self.wavePlotButton.width = changeValue - 350#Takes in new x window size and puts into wavePlot width
        self.testWavePlotter.updateGraph(self.seqStartStop[0],self.seqStartStop[1], (self.wavePlotButton.width)/100)
        self.wavePlotButton.reloadPic('C:/Users/jtmti/Documents/LightShow Project/Images/waveFile.jpg')

    def changeWaveStart(self,changeValue):
        if changeValue < 0:
            if self.seqStartStop[0] + changeValue < 0:
                self.seqStartStop[0] = 0
            else:
                self.seqStartStop[0] += changeValue
                self.seqStartStop[1] += changeValue
        elif changeValue > 0:
            self.seqStartStop[0] += changeValue
            self.seqStartStop[1] += changeValue
        self.testWavePlotter.updateGraph(self.seqStartStop[0],self.seqStartStop[1], (self.wavePlotButton.width)/100)
        self.wavePlotButton.reloadPic('C:/Users/jtmti/Documents/LightShow Project/Images/waveFile.jpg')


class runScreen():
    def __init__(self):
        self.windowDisplayValues = [1,1]

    def activeRun(self, win, width, height):
        self.windowDisplayValues = [width-315, height-95]

    def allEvent(self, event, pos):
        keys = pygame.key.get_pressed()



class displayScreen():
    def __init__(self):
        self.windowDisplayValues = [1,1]

    def activeRun(self, win, width, height):
        self.windowDisplayValues = [width-315, height-95]

    def allEvent(self, event, pos):
        keys = pygame.key.get_pressed()
        