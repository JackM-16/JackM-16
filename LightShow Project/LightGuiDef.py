import pygame
import time
import math
import tkinter
from tkinter import *
from tkinter import colorchooser
import ReadWriteDef

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
lightGrey2 = (150,150,150)
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

def textBox(win, objectButton):
    done = False
    #Activate Color
    objectButton.color = (objectButton.color[0] + 75,objectButton.color[1] + 75,objectButton.color[2] + 75)
    Textin = ''
    while done != True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if keys[pygame.K_RETURN]:
                done = True
            elif keys[pygame.K_BACKSPACE]:
                deleteLen = (len(Textin))
                print(deleteLen)
                Textin = Textin[:(deleteLen-2)]
            else:
                if (event.type==pygame.KEYDOWN):
                    Textin = Textin + event.unicode
               # Textin += chr(keys)
        objectButton.text = str(Textin)
        objectButton.draw(win)
        pygame.display.update()

    #Deactivate Color
    objectButton.color = (objectButton.color[0] - 25,objectButton.color[1] - 25,objectButton.color[2] - 25)
    objectButton.draw(win)
    #Return the text
    return(str(Textin))

def addLightLine(win,screen_w,screen_h,lightDict, textBoxButton):
    firstClick = True
    time.sleep(1)
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if keys[pygame.K_q]:
                break
                
            if keys[pygame.K_ESCAPE]:
                break
        if firstClick == False:
            drawStartPosition = (   int(startPosition[0] * (screen_w/5 * 4) + 5), int(startPosition[1] * (screen_h/5 * 4) + 40)    )
            pygame.draw.line(win,(200,200,200),drawStartPosition, pos, 4)
            #pygame.draw.line(win,(200,200,200),(((screen_w/5 * 4) - startPosition[0]),((screen_h/5 * 4) - startPosition[1])), pos, 4)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if firstClick == False:
                endPosition = pos
                endPosition = (   (pos[0] - 5) / (screen_w/5 * 4), (pos[1] - 40) / (screen_h/5 * 4)   )
                #endPosition = ((screen_w/5 * 4) - pos[0], (screen_h/5 * 4) - pos[1])
                break
            if firstClick == True:
                print("Connected")
                firstClick = False
                startPosition = pos
                startPosition = (   (pos[0] - 5) / (screen_w/5 * 4), (pos[1] - 40) / (screen_h/5 * 4)   )
                #startPosition = ((screen_w/5 * 4) - pos[0]-5, (screen_h/5 * 4) - pos[1]-40)
                time.sleep(.5)
    #numLights = input("Number of lights?")
    numLights = addLightNumber()
    if numLights != 0 :
        lightDict.append(lightLine((200,200,200), startPosition,endPosition, int(numLights)))

def addLightCirlce(win,screen_w,screen_h,lightDict):
    firstClick = True
    time.sleep(1)
    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if keys[pygame.K_q]:
                break
                
            if keys[pygame.K_ESCAPE]:
                break
        if firstClick == False:
            drawStartPosition = (   int(startPosition[0] * (screen_w/5 * 4) + 5), int(startPosition[1] * (screen_h/5 * 4) + 40)    )
            radiusDraw = abs( math.sqrt(((pos[0] - drawStartPosition[0])**2) + ((pos[1] - drawStartPosition[1])**2)))
            pygame.draw.circle(win, (200,200,200),drawStartPosition,int(radiusDraw))
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if firstClick == False:
                endPosition = (   (pos[0] - 5) / (screen_w/5 * 4), (pos[1] - 40) / (screen_h/5 * 4)   )
                break
            if firstClick == True:
                print("Connected")
                firstClick = False
                startPosition = pos
                startPosition = (   (pos[0] - 5) / (screen_w/5 * 4), (pos[1] - 40) / (screen_h/5 * 4)   )
                time.sleep(.5)
    numLights = addLightNumber()
    if numLights != 0 :
        lightDict.append(lightCircle((200,200,200),startPosition, endPosition,int(numLights)))

class lightLine():
    def __init__ (self, color, start, end, numLights):
        self.color = color
        self.start = start
        self.end = end
        self.numLights = numLights
        self.String =[]
        x = 0
        self.selected = False
        self.isPartOfConnector = False
        while x < numLights:
            self.String.append(self.color)
            x = x + 1
    def updateLoc(self,start,end):
        self.start = start
        self.end = end

    def getType(self):
        return("Line")

    def getLocationList(self,screen_w,screen_h):
        fullList = []
        
        drawStartPosition = (   int(self.start[0] * (screen_w/5 * 4) + 5), int(self.start[1] * (screen_h/5 * 4) + 40)    )
        drawEndPosition = (   int(self.end[0] * (screen_w/5 * 4) + 5), int(self.end[1] * (screen_h/5 * 4) + 40)    )
        xDistance = drawEndPosition[0] - drawStartPosition[0]
        yDistance = drawEndPosition[1] - drawStartPosition[1]
        i = 0
        move = drawStartPosition[0]
        ymove = drawStartPosition[1]
        while i < self.numLights:
            fullList.append(  [int(i), int(move), int(ymove+.5)]  )
            i = i + 1
            move = move + (xDistance/(self.numLights-1))
            ymove = ymove + (yDistance/(self.numLights-1))
        return(fullList)
    
    def draw(self,win,screen_w,screen_h):
        drawStartPosition = (   int(self.start[0] * (screen_w/5 * 4) + 5), int(self.start[1] * (screen_h/5 * 4) + 40)    )
        drawEndPosition = (   int(self.end[0] * (screen_w/5 * 4) + 5), int(self.end[1] * (screen_h/5 * 4) + 40)    )
        xDistance = drawEndPosition[0] - drawStartPosition[0]
        yDistance = drawEndPosition[1] - drawStartPosition[1]
        pygame.draw.line(win,self.color,(drawStartPosition), (drawEndPosition), 2)
        i = 0
        move = drawStartPosition[0]
        ymove = drawStartPosition[1]
        while i < self.numLights:
            if self.selected == True:
                pygame.draw.circle(win, (0,150,255),(int(move), int(ymove+.5)),8)
                
            pygame.draw.circle(win, (self.String[i]),(int(move),int(ymove+.5)),4)
            i = i + 1
            move = move + (xDistance/(self.numLights-1))
            ymove = ymove + (yDistance/(self.numLights-1))
        

class lightCircle():
    def __init__ (self, color,start, end, numLights):
        self.color = color
        self.start = start
        self.x = start[0]
        self.y = start[1]
        self.end = end
        self.numLights = numLights
        self.String =[]
        x = 0
        self.selected = False
        self.isPartOfConnector = False
        while x < numLights:
            self.String.append(self.color)
            x = x + 1
    def updateLoc(self,x,y):
        self.x = x
        self.y = y

    def getType(self):
        return("Circle")

    def getLocationList(self,screen_w,screen_h):
        fullList = []
        self.x = int(self.start[0] * (screen_w/5 * 4) + 5)
        self.y = int(self.start[1] * (screen_h/5 * 4) + 40)

        finalEndDraw = (   int(self.end[0] * (screen_w/5 * 4) + 5), int(self.end[1] * (screen_h/5 * 4) + 40)    )
        radiusMath = abs( math.sqrt(((finalEndDraw[0] - self.x)**2) + ((finalEndDraw[1] - self.y)**2)))
        i = 0
        PI = 3.141592653
        angle = 1.570796326
        while i < self.numLights:
            x = radiusMath * math.sin(angle) + self.x 
            y = radiusMath * math.cos(angle) + self.y
            
            fullList.append(  [int(i), int(x), int(y)]  )
            
            (360/self.numLights)* (PI/180)
            angle = angle + (360/self.numLights)* (PI/180)
            i = i +1
        return(fullList)
    
    def draw(self,win, screen_w,screen_h):
        self.x = int(self.start[0] * (screen_w/5 * 4) + 5)
        self.y = int(self.start[1] * (screen_h/5 * 4) + 40)
        
        pygame.draw.circle(win, (0,0,100),(self.x, self.y),4)

        finalEndDraw = (   int(self.end[0] * (screen_w/5 * 4) + 5), int(self.end[1] * (screen_h/5 * 4) + 40)    )
        radiusMath = abs( math.sqrt(((finalEndDraw[0] - self.x)**2) + ((finalEndDraw[1] - self.y)**2)))
        i = 0
        PI = 3.141592653
        angle = 1.570796326
        while i < self.numLights:
            x = radiusMath * math.sin(angle) + self.x 
            y = radiusMath * math.cos(angle) + self.y
            if self.selected == True:
                pygame.draw.circle(win, (0,150,255),(int(x), int(y)),8)
            pygame.draw.circle(win, self.String[i],(int(x), int(y)),4)
            
            (360/self.numLights)* (PI/180)
            angle = angle + (360/self.numLights)* (PI/180)
            i = i +1


class connector():
    def __init__ (self, x, y, inputLightObjects):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.lightObjects = inputLightObjects

    def getType(self):
        return("Connector")

    def getNumLights(self):
        totalLightCount = 0
        for obj in self.lightObjects:
            totalLightCount = obj.numLights + totalLightCount
        return(totalLightCount)

    def selected(self, isHighlighted):
        for obj in self.lightObjects:
            obj.selected = isHighlighted
    
    def connect(self,win, r, g, b, lightNum):
        if r > 0 or g > 0 or b > 0:
            x = 0
            previous = 0
            while x < len(self.lightObjects):
                currentObject = self.lightObjects[x]
                if (lightNum < currentObject.numLights + previous):
                    self.lightObjects[x].String[lightNum - previous] = (r,g,b)
                    currentObject.draw(win)
                    x = len(self.lightObjects)
                else:
                    previous = previous + currentObject.numLights
                x = x + 1         
        else:
            x = 0
            previous = 0
            while x < len(self.lightObjects):
                if (lightNum < self.lightObjects[x].numLights + previous):
                    self.lightObjects[x].String[lightNum - previous] = self.lightCount[x].color
                    self.lightObjects[x].draw(win)
                else:
                    previous = previous + self.lightCount[x].numLights
                x = x + 1


    def updateLightObjects(self, testList,win):
        timesRepeat = len(testList)
        x = 0
        self.lightObjects = []
        while x < timesRepeat:
            self.lightObjects.append(testList[x])
            x = x +1
        #testList[0].lightColor(win,255,255,40,24)
        print(self.lightObjects)

        
    def updateLoc(self,x,y):
        self.x = x
        self.y = y
        
    def draw(self,win, screen_w,screen_h,outline = None):
        #Call this method to draw the button on the screen
        
##        for lights in self.lightObjects:
##            lights.draw(win,screen_w,screen_h)
        
        if outline:
            pygame.draw.rect(win, outline, (self.x-4,self.y-4,self.width+8,self.height+8),0)

        pygame.draw.rect(win, (0,0,150), (self.x,self.y,self.width,self.height),0)

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class cubeArray():
    def __init__(self,lengthSong,numObjects,startX,startY):
        self.WIDTH = 30
        self.HEIGHT = 30
        # This sets the margin between each cell
        self.MARGIN = 5
        self.row = numObjects
        self.column = lengthSong
        self.x = startX
        self.y = startY

        self.grid = []
        for row in range(self.row):
            # Add an empty array that will hold each cell
            # in this row
            self.grid.append([])
            for column in range(self.column):
                self.grid[row].append((255,255,255))  # Append a cell

        
    def draw(self,win, rectlength):
        for r in range(self.row):
            for c in range(self.column):
                if ((self.WIDTH + self.MARGIN)*c + self.x) + self.WIDTH < rectlength:
                    color = self.grid[r][c]
                    pygame.draw.rect(win,color,((self.WIDTH + self.MARGIN)*c + self.x,(self.HEIGHT + self.MARGIN)*r + self.y,self.WIDTH,self.HEIGHT))

    def addObject(self,color,pos):
        ## Set row 1, cell 5 to one. (Remember rows and
        ## column numbers start at zero.)
        #grid[1][5] = 1
        # Change the x/y screen coordinates to grid coordinates
        column = (pos[0]- self.x) // (self.WIDTH + self.MARGIN)
        row = (pos[1] - self.y) // (self.HEIGHT + self.MARGIN)
        # Set that location to one
        self.grid[row][column] = color
        
    def isOverSubject(self, pos):
        column = (pos[0]- self.x) // (self.WIDTH + self.MARGIN)
        row = (pos[1] - self.y) // (self.HEIGHT + self.MARGIN)
        if row < len(self.grid) and row > -1:
            if column < len(self.grid[row]) and column > -1:
                return(True)
        return(False)

class itemArray():
    def __init__(self, newX, newY):
        self.startX = newX
        self.startY = newY
        self.width = 1
        self.height = 40
        self.margin = 5
        self.edit = False
        self.currentTime = 0
        self.dict = {}
        self.selected = []
        self.scrollUpButton = Button((50,50,50), 1, (0,0,0), text = '')
        self.scrollDownButton = Button((50,50,50), 1, (0,0,0), text = '')
        self.ScrolledDistance = 0
        self.lastTime = 0
        self.changeSelectedButton = Button((50,50,50), 25, (255,255,255), text = 'CHANGE')
        self.curent_full_list = []

    def updateLocation(self, newX, newY):
        self.startX = newX
        self.startY = newY

    def editItems(self):
        if self.edit == False:
            self.edit = True
        else:
            self.edit = False

    def addItem(self, newList):
        readFrom = addColorLight(newList)
        newColorFull = readFrom[0]
        for numbers in readFrom[1]:
             ReadWriteDef.addPixel(self.dict, self.currentTime, numbers, newColorFull[0], newColorFull[1], newColorFull[2])
##        for Objects in range(len(self.selected)):
##            selected_object_number = self.selected[Objects]
##            ReadWriteDef.addPixel(self.dict, self.currentTime, self.curent_full_list[selected_object_number], newColorFull[0], newColorFull[1], newColorFull[2])
            
    def clickChangeSelected(self, pos):
        if self.changeSelectedButton.isOver(pos):
            if len(self.selected) > 0:
                newColorFull = colorWheel()
                for Objects in range(len(self.selected)):
                    selected_object_number = self.selected[Objects]
                    ReadWriteDef.addPixel(self.dict, self.currentTime, self.curent_full_list[selected_object_number], newColorFull[0], newColorFull[1], newColorFull[2])

    def hoverChangeSelected(self, pos, win):
        if self.changeSelectedButton.isOver(pos):
            self.changeSelectedButton.draw(win, ((255,255,255)))
            
    def clickItems(self, pos):
        if self.edit == True:
            if pos[0] > self.startX - 32 and pos[0] < self.startX + 10:
                selcetedNumber = (    ((pos[1] - self.startY) + (self.ScrolledDistance*(self.height + self.margin))) // (self.height + self.margin)    )
                if (selcetedNumber - 1) in self.selected:
                    self.selected.remove(selcetedNumber - 1)
                else:
                    self.selected.append(selcetedNumber - 1)
        
    def clickScroll(self, pos):
        if self.scrollUpButton.isOver(pos):
            self.ScrolledDistance = self.ScrolledDistance - 1
        if self.scrollDownButton.isOver(pos):
            self.ScrolledDistance = self.ScrolledDistance + 1

    def draw(self, win, width, maxHeight, time, dictName):
        if time != self.lastTime:
            self.ScrolledDistance = 0
            self.selected = []
        self.lastTime = time
        
        self.currentTime = time
        self.dict = dictName

        width2 = width
        if self.edit == True:
           width2 = width - 110
           self.changeSelectedButton.updateLoc(self.startX + width2 + 5,self.startY ,105, self.height)
           self.changeSelectedButton.draw(win, ())
            
        pygame.draw.rect(win, (50,50,50), (self.startX, self.startY ,width2 ,self.height),0)
        font = pygame.font.SysFont('comicsans', 40)
        text = font.render(str(time), 1, (255,255,255))
        win.blit(text, (self.startX + int(width2/2 - text.get_width()/2), self.startY + int(self.height/2 - text.get_height()/2)))

        if self.edit == True:
            self.startX = self.startX + 32
            width = width - 32
            
        returnedDict = findAllLights(dictName, time)
        testDrawFind = self.startY + ((self.height)* (len(returnedDict)-1)) + self.margin * (len(returnedDict)-1)
        if (testDrawFind + self.margin + self.height) > (maxHeight - self.startY):
            widthExtra = 10
            SlideBar = True
        else:
            widthExtra = 0
            SlideBar = False

        listOfItems = [0,0]
        itemList = list(returnedDict.keys())
        itemList.sort()
        self.curent_full_list = itemList
        
        for XI in range(len(returnedDict)):
            pinNumber = itemList[XI]
            itemSearch = itemList[XI]
            
            itemType = (returnedDict[itemSearch][0])
            R = int(returnedDict[itemSearch][1])
            G = int(returnedDict[itemSearch][2])
            B = int(returnedDict[itemSearch][3])
            I = XI + 1
            
            writeText = str(itemType) +", " +  str(pinNumber)

            drawHeight = (self.startY + ((self.height)* I) + self.margin * I)
            
            #-------------------------------------------------------------------#
            if drawHeight + (self.height + self.margin) >= maxHeight:
                listOfItems[1] = listOfItems[1] + 1
            else:
                listOfItems[0] = listOfItems[0] + 1

            drawHeight = (self.startY + ((self.height)* I) + self.margin * I) - (self.ScrolledDistance*(self.height + self.margin))

            if drawHeight > self.startY + (self.height - 10):
                pygame.draw.rect(win, (50,50,50), (self.startX, drawHeight,width - widthExtra,self.height),0)
                font = pygame.font.SysFont('comicsans', 30)
                text = font.render(writeText, 1, (R,G,B))
                win.blit(text, (self.startX + int((width - widthExtra)/2 - text.get_width()/2), drawHeight + int(self.height/2 - text.get_height()/2)))
                    
            if self.edit == True:
                if drawHeight > self.startY + (self.height - 10):
                    pygame.draw.circle(win, (75,75,75),(int(self.startX -16), int(drawHeight + 20)),12)
                    if (I - 1) in self.selected:
                        pygame.draw.circle(win, (0,150,255),(int(self.startX -16), int(drawHeight + 20)),10)
                    else:
                        pygame.draw.circle(win, (255,255,255),(int(self.startX -16), int(drawHeight + 20)),10)
        
        if SlideBar == True: 
##            pygame.draw.rect(win, (125,125,125), (self.startX +5+(width - widthExtra), self.startY + self.height + self.margin ,8,maxHeight - self.startY - self.height - 10),0)
##            heightOfScrollBar = (maxHeight - self.startY - self.height - 10) * (listOfItems[0]/(listOfItems[0] + listOfItems[1]))
##            #pygame.draw.rect(win, (50,50,50), (self.startX +5+(width - widthExtra), self.startY + self.height + self.margin ,8, int(heightOfScrollBar)),0)
##            self.scrollBarButton.updateLoc(self.startX +5+(width - widthExtra),self.startY + self.height + self.margin + (self.ScrolledDistance * (int(heightOfScrollBar) / (listOfItems[0] + listOfItems[1]))),8,int(heightOfScrollBar))
##            self.scrollBarButton.draw(win,())

            self.scrollUpButton.updateLoc(self.startX +5+(width - widthExtra),self.startY + self.height + self.margin,8,50)
            self.scrollDownButton.updateLoc(self.startX +5+(width - widthExtra),(self.startY + self.height + self.margin)*2,8,50)
            self.scrollUpButton.draw(win,())
            self.scrollDownButton.draw(win,())
            
            #pygame.draw.rect(win, (50,50,50), (self.startX +5+(width - widthExtra), self.startY + self.height + self.margin ,8,testDrawFind - 100),0)



class lightConnectorArray():
    def __init__(self, newX, newY):
        self.startX = newX
        self.startY = newY
        self.width = 1
        self.height = 40
        self.margin = 5
        self.objectSelection = 0
        self.lsit = []
        self.selected = []
        self.scrollBarButton = Button((50,50,50), 1, (0,0,0), text = '')
        self.ScrolledDistance = 0
        self.lastTime = 0
        self.changeSelectedButton = Button((50,50,50), 25, (255,255,255), text = 'EDIT')
        self.curent_full_list = []
        self.MaxScroll = False
        self.minScroll = False
        self.fullScrollBarLine = Button((125,125,125), 25, (255,255,255), text = '')
        
    def updateLocation(self, newX, newY):
        self.startX = newX
        self.startY = newY
            
    def clickChangeSelected(self, pos):
        if self.changeSelectedButton.isOver(pos):
            if len(self.selected) > 0:
                newColorFull = colorWheel()
                for Objects in range(len(self.selected)):
                    selected_object_number = self.selected[Objects]
                    ReadWriteDef.addPixel(self.dict, self.currentTime, self.curent_full_list[selected_object_number], newColorFull[0], newColorFull[1], newColorFull[2])

    def hoverChangeSelected(self, pos, win):
        if self.changeSelectedButton.isOver(pos):
            self.changeSelectedButton.draw(win, ((255,255,255)))
            
    def clickItems(self, pos):
        if pos[0] > self.startX - 32 and pos[0] < self.startX + 10:
            selcetedNumber = (    ((pos[1] - self.startY) + (self.ScrolledDistance*(self.height + self.margin))) // (self.height + self.margin)    )
            if (selcetedNumber - 1) in self.selected:
                self.selected.remove(selcetedNumber - 1)
            else:
                self.selected.append(selcetedNumber -1)
        if len(self.selected) > 1:
            self.selected.pop(0)
        pygame.time.wait(100)

    def returnClickedItems(self):
        return(self.selected)
        
    def clickScroll(self, pos):
        if self.fullScrollBarLine.isOver(pos):
            if pos[1] < (self.fullScrollBarLine.y + (self.fullScrollBarLine.height/2)) and self.minScroll == False:
                self.ScrolledDistance = self.ScrolledDistance - 1
            elif pos[1] > ((self.fullScrollBarLine.y + (self.fullScrollBarLine.height/2))) and self.MaxScroll == False:
                self.ScrolledDistance = self.ScrolledDistance + 1

    def draw(self, win, width, maxHeight, inputObject, inList):
        ## Dict Format == {:[]}
        if time != self.lastTime:
            self.ScrolledDistance = 0
            self.selected = []
        self.lastTime = time
        
        self.objectSelection = inputObject
        self.list = inList
        
        width2 = width - 110
        self.changeSelectedButton.updateLoc(self.startX + width2 + 5,self.startY ,105, self.height)
        self.changeSelectedButton.draw(win, ())
        
            
        pygame.draw.rect(win, (50,50,50), (self.startX, self.startY ,width2 ,self.height),0)
        if inputObject != None:
            font = pygame.font.SysFont('comicsans', 35)
            text = font.render((str(self.objectSelection.getType()) + "  " + str(self.objectSelection.numLights)), 1, (255,255,255))
            win.blit(text, (self.startX + int(width2/2 - text.get_width()/2), self.startY + int(self.height/2 - text.get_height()/2)))

        
        self.startX = self.startX + 32
        width = width - 32
            
        testDrawFind = self.startY + ((self.height)* (len(inList)-1)) + self.margin * (len(inList)-1)
        if (testDrawFind + self.margin + self.height) > (maxHeight - self.startY):
            widthExtra = 10
            SlideBar = True
        else:
            widthExtra = 0
            SlideBar = False

        listOfItems = [0,0]
        self.curent_full_list = inList
        
        for XI in range(len(inList)):
            itemType = inList[XI].getType()
            if itemType != "Connector":
                lightCount = inList[XI].numLights
            else:
                lightCount = self.list[XI].getNumLights()
            
            I = XI + 1
            
            writeText = str(itemType) +", " +  str(lightCount)

            drawHeight = (self.startY + ((self.height)* I) + self.margin * I)
            
            #-------------------------------------------------------------------#
            if drawHeight + (self.height + self.margin) >= maxHeight:
                listOfItems[1] = listOfItems[1] + 1
            else:
                listOfItems[0] = listOfItems[0] + 1

            drawHeight = (self.startY + ((self.height)* I) + self.margin * I) - (self.ScrolledDistance*(self.height + self.margin))

            if drawHeight > self.startY + (self.height - 10):
                if drawHeight + self.height < maxHeight:
                    pygame.draw.rect(win, (50,50,50), (self.startX, drawHeight,width - widthExtra,self.height),0)
                    font = pygame.font.SysFont('comicsans', 30)
                    text = font.render(writeText, 1, (255,255,255))
                    win.blit(text, (self.startX + int((width - widthExtra)/2 - text.get_width()/2), drawHeight + int(self.height/2 - text.get_height()/2)))
                    
            
            if drawHeight > self.startY + (self.height - 10):
                if drawHeight + self.height < maxHeight:
                    pygame.draw.circle(win, (75,75,75),(int(self.startX -16), int(drawHeight + 20)),12)
                    if (I - 1) in self.selected:
                        pygame.draw.circle(win, (0,150,255),(int(self.startX -16), int(drawHeight + 20)),10)
                    else:
                        pygame.draw.circle(win, (255,255,255),(int(self.startX -16), int(drawHeight + 20)),10)
        
        if SlideBar == True:
            self.fullScrollBarLine.updateLoc(self.startX +5+(width - widthExtra), self.startY + self.height + self.margin ,8,maxHeight - self.startY - self.height - 10)
            self.fullScrollBarLine.draw(win)
            #pygame.draw.rect(win, (125,125,125), (self.startX +5+(width - widthExtra), self.startY + self.height + self.margin ,8,maxHeight - self.startY - self.height - 10),0)
            heightOfScrollBar = (maxHeight - self.startY - self.height - 10) * (listOfItems[0]/(listOfItems[0] + listOfItems[1]))

            scrollStartLocation = self.startY + self.height + self.margin + (self.ScrolledDistance * (int(heightOfScrollBar) / (listOfItems[0] + listOfItems[1])))
            if scrollStartLocation + heightOfScrollBar < maxHeight:
                self.MaxScroll = False
                self.scrollBarButton.updateLoc(self.startX +5+(width - widthExtra),scrollStartLocation,8,int(heightOfScrollBar))
            else:
                self.MaxScroll = True

            if self.scrollBarButton.y <= self.height + self.startY + self.margin:
                self.minScroll = True
                self.scrollBarButton.updateLoc(self.startX +5+(width - widthExtra),self.height + self.startY + self.margin,8,int(heightOfScrollBar))
            else:
                self.minScroll = False
                
            self.scrollBarButton.draw(win,())


def findAllLights(dictName, endTime):
    returnList = {}
    currentTime =  0
    while currentTime <= endTime:
        if currentTime in dictName:
            timeRepeat = dictName[currentTime][0]
            I = 0
            itemNumber = dictName[currentTime]
            while I < timeRepeat:
                I = I + 1
                itemType = itemNumber[I][0]
                pinNumber = itemNumber[I][1]
                R = int(itemNumber[I][2])
                G = int(itemNumber[I][3])
                B = int(itemNumber[I][4])
                writeText = [itemType, R, G, B]
                if (R > 0 or G > 0 or B > 0):
                    returnList[pinNumber] = writeText
                else:
                    if pinNumber in returnList:
                        del returnList[pinNumber]
            

                
        currentTime = round(currentTime + .01, 2)
    return(returnList)
        
def colorWheel():
    root = Tk()
    root.title("Pixel Editor")
    root.geometry("200x200")
    def color():
        global listColorsClickedGlobal
        my_color = colorchooser.askcolor()
        colorR = int(my_color[0][0])
        colorG = int(my_color[0][1])
        colorB = int(my_color[0][2])
        #my_label = Label(root, text=[colorR, colorG, colorB]).pack(pady=10)
        my_label2 = Label(root, text="                ", font=("Helvetica", 10), bg=my_color[1]).pack()
        listColorsClickedGlobal = [colorR, colorG, colorB]
        
    my_button = tkinter.Button(root, text="Pick A Color", command=color).pack()
    
    root.mainloop()
    return(listColorsClickedGlobal)


def addColorLight(newListInput):
    FirstTime = True
    root = Tk()
    root.title("Pixel Creater")
    root.geometry("325x225")
    SelectedListItems = []
    def color():
        global listColorsClickedGlobal
        my_color = colorchooser.askcolor()
        colorR = int(my_color[0][0])
        colorG = int(my_color[0][1])
        colorB = int(my_color[0][2])
        #my_label = Label(root, text=[colorR, colorG, colorB]).pack(pady=10)
        my_label2 = Label(root, text="  ", font=("Helvetica", 100), bg=my_color[1])
        my_label2.grid(row = 1, column = 0, sticky = W)
        listColorsClickedGlobal = [colorR, colorG, colorB]
        
    def show():
        ScrollBarButton = Scrollbar(root)
        mylist = Listbox(root, yscrollcommand = ScrollBarButton.set )
        SelectedListItemsGlobal.sort()
        for line in range(len(SelectedListItemsGlobal)):  
            mylist.insert(END, "Pin " + str(SelectedListItemsGlobal[line]))  
        mylist.grid(row = 1, column = 3, sticky = W)

    def addToList():
        objectSelection = my_listBox.curselection()
        for items in objectSelection:
            curentObject = LightOptions[items]
            if items not in SelectedListItemsIndex:
                SelectedListItemsGlobal.append(curentObject)
                SelectedListItemsIndex.append(items)
        show()

    def selectAllItems():
        for items in range(len(LightOptions)):
            if items not in SelectedListItemsIndex:
                SelectedListItemsGlobal.append(LightOptions[items])
                SelectedListItemsIndex.append(items)
        show()
    def deleteAllItems():
        SelectedListItemsGlobal.clear()
        SelectedListItemsIndex.clear()
        show()
    def selectOddItems():
        for x in range(len(LightOptions)):
            if LightOptions[x]%2 != 0:
                if x not in SelectedListItemsIndex:
                    SelectedListItemsIndex.append(x)
                    SelectedListItemsGlobal.append(LightOptions[x])
        show()
    def selectEvenItems():
        for x in range(len(LightOptions)):
            if LightOptions[x]%2 == 0:
                if x not in SelectedListItemsIndex:
                    SelectedListItemsIndex.append(x)
                    SelectedListItemsGlobal.append(LightOptions[x])
        show()

    LightOptions = newListInput
##    clicked = StringVar()
##    clicked.set(LightOptions[0])
##    drop = OptionMenu(root, clicked, *LightOptions)
##    drop.grid(row = 0, column = 1, sticky = W, pady = 2)

    SelectedListItemsGlobal=[]
    SelectedListItemsIndex=[]
    ###----------###
    my_listBox = Listbox(root, selectmode=MULTIPLE)
    
    my_listBox.grid(row = 1, column = 1)
    
    #my_listBox.insert(END, "First Item")
    for item in LightOptions:
        my_listBox.insert(END, "Pin " + str(item))
    ###----------###

    show_Button = tkinter.Button(root, text="Show Selection", command=show)
    color_button = tkinter.Button(root, text="Pick All Color", command=color)
    addTo_button = tkinter.Button(root, text="Add", command=addToList)
    selectAll_button = tkinter.Button(root, text="All", command=selectAllItems)
    deleteAll_button = tkinter.Button(root, text="Del", command=deleteAllItems)
    allEven_button = tkinter.Button(root, text="Even", command=selectEvenItems)
    allOdd_button = tkinter.Button(root, text="Odd", command=selectOddItems)

    color_button.grid(row = 0, column = 0)
    addTo_button.grid(row = 0, column = 2)
    show_Button.grid(row = 0, column = 3)
    selectAll_button.grid(row = 0, column = 1, sticky = 'W')
    deleteAll_button.grid(row = 0, column = 1, sticky = 'W', padx=25)
    allEven_button.grid(row = 0, column = 1, sticky = 'W', padx=54)
    allOdd_button.grid(row = 0, column = 1,sticky = 'E', padx=20)

    root.mainloop()
    return listColorsClickedGlobal, SelectedListItemsGlobal



def ConnectorGUI(ConnectorOptions):
    root = Tk()
    root.title("Connector")
    root.geometry("325x225")
    SelectedListItems = []

    def show():
        ScrollBarButton = Scrollbar(root)
        mylist = Listbox(root, yscrollcommand = ScrollBarButton.set )
        for line in range(len(SelectedListItemsGlobal)):
            LightType = str(SelectedListItemsGlobal[line].getType())
            NumLights = str(SelectedListItemsGlobal[line].numLights)
            mylist.insert(END, LightType + " " + NumLights)  
        mylist.grid(row = 1, column = 3, sticky = W)

    def addToList():
        objectSelection = my_listBox.curselection()
        for items in objectSelection:
            curentObject = ConnectorOptions[items]
            if curentObject not in SelectedListItemsGlobal:
                SelectedListItemsGlobal.append(curentObject)
        show()

    def deleteAllItems():
        SelectedListItemsGlobal.clear()
        show()

    SelectedListItemsGlobal=[]
    ###----------###
    my_listBox = Listbox(root, selectmode=MULTIPLE)
    
    my_listBox.grid(row = 1, column = 0)
    
    #my_listBox.insert(END, "First Item")
    for item in ConnectorOptions:
        LightType = str(item.getType())
        NumLights = str(item.numLights)
        my_listBox.insert(END, LightType + " " + NumLights)
    ###----------###
        
    directionLabel = Label(root, text="Add In Order", font=("Helvetica", 10) )
    addTo_button = tkinter.Button(root, text="Add", command=addToList)
    deleteAll_button = tkinter.Button(root, text="Del", command=deleteAllItems)

    directionLabel.grid(row = 0, column = 0)
    addTo_button.grid(row = 0, column = 1)
    deleteAll_button.grid(row = 0, column = 2)

    root.mainloop()
    for names in SelectedListItemsGlobal:
        names.isPartOfConnector = True
        #ConnectorOptions.remove(names)
    return SelectedListItemsGlobal


def addLightNumObject(win, inputObject, drawStartX, drawStartY, drawHeight):
    root = Tk()
    root.title("Connector")
    root.geometry("325x225")
    SelectedListItems = []

    def show():
        ScrollBarButton = Scrollbar(root)
        mylist = Listbox(root, yscrollcommand = ScrollBarButton.set )
        for line in range(len(SelectedListItemsGlobal)):
            LightType = str(SelectedListItemsGlobal[line].getType())
            NumLights = str(SelectedListItemsGlobal[line].numLights)
            mylist.insert(END, LightType + " " + NumLights)  
        mylist.grid(row = 1, column = 3, sticky = W)

    def addToList():
        objectSelection = my_listBox.curselection()
        for items in objectSelection:
            curentObject = ConnectorOptions[items]
            if curentObject not in SelectedListItemsGlobal:
                SelectedListItemsGlobal.append(curentObject)
        show()

    def deleteAllItems():
        SelectedListItemsGlobal.clear()
        show()

    SelectedListItemsGlobal=[]
    ###----------###
    my_listBox = Listbox(root, selectmode=MULTIPLE)
    
    my_listBox.grid(row = 1, column = 0)
    
    #my_listBox.insert(END, "First Item")
    for item in ConnectorOptions:
        LightType = str(item.getType())
        NumLights = str(item.numLights)
        my_listBox.insert(END, LightType + " " + NumLights)
    ###----------###
        
    directionLabel = Label(root, text="Add In Order", font=("Helvetica", 10) )
    addTo_button = tkinter.Button(root, text="Add", command=addToList)
    deleteAll_button = tkinter.Button(root, text="Del", command=deleteAllItems)

    directionLabel.grid(row = 0, column = 0)
    addTo_button.grid(row = 0, column = 1)
    deleteAll_button.grid(row = 0, column = 2)

    root.mainloop()
    return SelectedListItemsGlobal

def addLightNumber():
    root = Tk()
    root.title("Connector")
    root.geometry("325x225")
    
    def number():
        try:
            int(textBox.get())
            global finalNumber
            finalNumber = 0
            finalNumber = int(textBox.get())
            root.destroy()
        except ValueError:
            finalNumber = 0
            print("Not a real number")
        
    enterLabel = Label(root, text="Light Number", font=("Helvetica", 10) )
    cancelLabel = Label(root, text="0 to Cancel", font=("Helvetica", 10) )
    textBox = tkinter.Entry(root)
    buttonEnter = tkinter.Button(root, text="Enter", command=number)

    enterLabel.grid(row = 0, column = 0)
    textBox.grid(row = 1, column = 0)
    buttonEnter.grid(row = 2, column = 0)
    cancelLabel.grid(row = 1, column = 1)

    root.mainloop()
    print(finalNumber)
    return(finalNumber)

def tupleStart():
        try:
            global finalStartTuple
            firstHalf=""
            secondHalf = ""
            testInNumber = tuple(startTextBox.get())
            for number in testInNumber:
                if number!= "," :
                    firstHalf+= number
                else:
                    break
            for Numbers in range(len(firstHalf) + 1, len(testInNumber)):
                secondHalf+=testInNumber[Numbers]

            finalFirstHalf = int(firstHalf)
            finalSecondHalf = int(secondHalf)
            finalStartTuple = (finalFirstHalf,finalSecondHalf)
            start = finalStartTuple
        except ValueError:
            print("Not a real number")

def inBoxLight(lightList, startX, startY, width, height):
    lightNumber = 0
    lightStartX = 1
    lightStartY = 2
    lightNumsInside = []
    for lists in lightList:
        if (lists[lightStartX] > startX) and (lists[lightStartX] < startX+width) and (lists[lightStartY] > startY) and (lists[lightStartY] < startY+height):
            lightNumsInside.append(lists[lightNumber])
    return(lightNumsInside)


def formatLightsForAddArray(lightArray, connectionsArray):
    finalReturnLights = []
    for lights in lightArray:
        startCount = 0
        print(lights.numLights)
        if lights.isPartOfConnector == False:
            for numbers in range(lights.numLights):
                finalReturnLights.append(startCount)
                startCount = startCount +1
    for objects in connectionsArray:
        startCount = 0
        print(objects.getNumLights())
        for numbers in range(objects.getNumLights()):
            finalReturnLights.append(startCount)
            startCount = startCount +1
    return(finalReturnLights)
        





class listBox():
    def __init__ (self,highlightColor, text_height, textColor, listofObjects):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.highlightColor = highlightColor
        self.text_height = text_height
        self.textColor = textColor
        self.listofObjects = listofObjects
        self.ScrollBar2 = ScrollBar2()
        self.highlightedNum = -1

    def updateLoc(self,x,y,width,height):
        self.x =int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        image_height = self.y +5+((len(self.listofObjects)-1)*self.text_height)
        self.ScrollBar2.update(self.x, self.y, self.width, self.height, 500, 5+self.text_height)
        
    def draw(self,win,outline = None):
        #Call this method to draw the button on the screen
        pygame.draw.rect(win, (255,255,255), (self.x,self.y,self.width,self.height),0)
        if self.listofObjects != []:
            for x in range(len(self.listofObjects)):
                font = pygame.font.SysFont('comicsans', self.text_height)
                text = font.render(self.listofObjects[x], 1, (self.textColor))
                if self.highlightedNum == x:
                    pygame.draw.rect(win, (100,100,100), (self.x, self.y+(x*self.text_height),self.width,self.text_height),0)
                if self.y +5+(x*self.text_height)+self.text_height <self.y+self.height:
                    win.blit(text, (self.x+5, self.y +5+(x*self.text_height)))
        self.ScrollBar2.draw(win)
                            
    def eventHandler(self, event):
        self.ScrollBar2.event_handler(event)
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width-20:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousey = pos[1]-self.y
                    diffHeight = (int(self.y +5+((len(self.listofObjects)-1)*self.text_height))//len(self.listofObjects))
                    if self.highlightedNum == mousey//diffHeight:
                        self.highlightedNum = -1
                        time.sleep(.25)
                    else:
                        self.highlightedNum = mousey//diffHeight
                        time.sleep(.25)
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.K_UP:
                self.highlightedNum = self.highlightedNum -1
            if event.type == pygame.K_DOWN:
                self.highlightedNum = self.highlightedNum +1
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False


class ScrollBar(object):
    def __init__(self):
        self.y_axis = 0
        self.image_height = 0
        self.change_y = 0
        
        bar_height = 0
        self.bar_rect = 0
        self.bar_up = 0
        self.bar_down = 0
        
        self.bar_up_image = pygame.image.load("C:/Users/jtmti/Documents/Python/Scrollbar Test/up.png").convert()
        self.bar_down_image = pygame.image.load("C:/Users/jtmti/Documents/Python/Scrollbar Test/down.png").convert()
        
        self.on_bar = False
        self.mouse_diff = 0
        
    def update(self, y,SCREEN_WIDTH, SCREEN_HEIGHT, image_height):
        self.image_height = image_height
        bar_height = int((SCREEN_HEIGHT - 40) / (image_height / (SCREEN_HEIGHT * 1.0)))
        self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20,y+20,20,bar_height)
        self.bar_up = pygame.Rect(SCREEN_WIDTH - 20,0,20,20)
        self.bar_down = pygame.Rect(SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20,20,20)
        
        self.y_axis += self.change_y
        
        if self.y_axis > 0:
            self.y_axis = 0
        elif (self.y_axis + self.image_height) < SCREEN_HEIGHT:
            self.y_axis = SCREEN_HEIGHT - self.image_height
            
        height_diff = self.image_height - SCREEN_HEIGHT
        
        scroll_length = SCREEN_HEIGHT - self.bar_rect.height - 40
        bar_half_lenght = self.bar_rect.height / 2 + 20
        
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < y+20:
                self.bar_rect.top = y+20
            elif self.bar_rect.bottom > (SCREEN_HEIGHT - 20):
                self.bar_rect.bottom = SCREEN_HEIGHT - 20
            
            self.y_axis = int(height_diff / (scroll_length * 1.0) * (self.bar_rect.centery - bar_half_lenght) * -1)
        else:
            self.bar_rect.centery =  bar_half_lenght+y#scroll_length / (height_diff * 1.0) * (self.y_axis * -1) + bar_half_lenght
             
        
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(self.bar_up.center)
            print(pos)
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            if pos[0] > self.bar_up.center[0]-10 and pos[0] < self.bar_up.center[0]+10:
                print("True 1")
                if pos[1] > self.bar_up.center[1]+10 and pos[1] < self.bar_up.center[1]-10:
                    print("up")
                    self.change_y = 5
            elif self.bar_down.collidepoint(pos):
                self.change_y = -5
                
        if event.type == pygame.MOUSEBUTTONUP:
            self.change_y = 0
            self.on_bar = False
                
    def draw(self,screen,y, SCREEN_WIDTH, SCREEN_HEIGHT):
        pygame.draw.rect(screen,(50,50,50),self.bar_rect)
        
        screen.blit(self.bar_up_image,(SCREEN_WIDTH - 20,y))
        screen.blit(self.bar_down_image,(SCREEN_WIDTH - 20,SCREEN_HEIGHT - 20))


class ScrollBar2():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.snapHeight = 0
        self.objectHeight = 0
        self.bar_rect = pygame.Rect(1,1,20,50)
        self.upRect = pygame.Rect(1,1,20,20)
        self.downRect = pygame.Rect(1,1,20,20)
        self.change_y=0
        
        self.bar_up_image = pygame.image.load("C:/Users/jtmti/Documents/Python/Scrollbar Test/up.png").convert()
        self.bar_down_image = pygame.image.load("C:/Users/jtmti/Documents/Python/Scrollbar Test/down.png").convert()
        self.mouse_diff = 0
        self.on_bar = False
        
    def update(self,x,y,width,height, length, snapLength):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.objectHeight = length
        self.snapHeight = snapLength

        self.bar_rect = pygame.Rect(self.width-13,(self.y+20)+self.change_y,16,(self.height/self.objectHeight)*self.height)
        if self.on_bar:
            pos = pygame.mouse.get_pos()
            self.bar_rect.y = pos[1] - self.mouse_diff
            if self.bar_rect.top < self.y+20:
                self.bar_rect.top = self.y+20
            elif self.bar_rect.bottom > (self.y+self.height - 20):
                self.bar_rect.bottom = self.y+self.height - 20
            self.change_y = self.bar_rect.y-60

        self.upRect = pygame.Rect(self.width-15,self.y,20,20)
        self.downRect = pygame.Rect(self.width-15,self.height+self.y-20,20,20)
        
        #self.bar_rect = pygame.Rect(self.width-13,(self.y+20)+self.snapHeight*self.change_y,16,(self.height/self.objectHeight)*self.height)
    def event_handler(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print("Scroll up")
            if event.button == 4:
                print("Scroll down")
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            if self.upRect.collidepoint(pos):
                print("Over up")
                self.change_y -= self.snapHeight
            if self.downRect.collidepoint(pos):
                print("Over down")
                self.change_y += self.snapHeight
        if event.type == pygame.MOUSEBUTTONUP:
            self.on_bar = False

                
    def draw(self,screen):
        pygame.draw.rect(screen,(150,150,150),(self.width-15,self.y+20,20,self.height-40))
        
        pygame.draw.rect(screen,(200,200,200),self.bar_rect)
        if self.on_bar == True:
            pygame.draw.rect(screen,(75,75,75),self.bar_rect)
        
        screen.blit(self.bar_up_image,(self.width-15,self.y))
        screen.blit(self.bar_down_image,(self.width-15,self.height+self.y-20))


















