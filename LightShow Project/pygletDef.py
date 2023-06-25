import pyglet
from pyglet import shapes
from pyglet.window import key, mouse

class Button():
    def __init__ (self, colorIn, text_height, textColor, text = ''):
        self.color = colorIn
        self.text_height = text_height
        self.textColor = textColor
        self.text = text
        self.over = False

        self.x = 1
        self.y = 1
        self.width = 1
        self.height = 1

        self.rect = shapes.Rectangle(1,1,1,1, color=colorIn)
        self.outline = shapes.Rectangle(1,1,1,1, color=(255, 255, 255))
        self.textLabel = pyglet.text.Label(text, font_size = text_height, color=textColor, font_name='Arial',anchor_x='center', anchor_y='center')

    def updateLoc(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height

        self.outline.x = x-4
        self.outline.y = y-4
        self.outline.width = width+8
        self.outline.height = height+8

        self.textLabel.x = x + width//2
        self.textLabel.y = y + height//2
        
    def draw(self,outline = None):
        #Call this method to draw the button on the screen
        if outline or self.over == True:
            self.outline.draw()

        self.rect.draw()

        if self.text != '':
            self.textLabel.draw()

    def isOver(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
            
        return False


class toggleButton():
    def __init__ (self, colorIn, highLightColor, text_height, textColor, text1 = '', text2 = ''):
        self.color = colorIn
        self.text_height = text_height
        self.textColor = textColor
        self.text = text1
        self.text2 = text2
        self.over = False
        self.highLightColor = highLightColor
        self.selectedItem = 0 #(0 or 1)

        self.x = 1
        self.y = 1
        self.width = 1
        self.height = 1

        self.outline = shapes.Rectangle(1,1,1,1, color=(255, 255, 255))

        self.leftToggle = Button(colorIn, self.text_height, textColor, self.text)
        self.rightToggle = Button(colorIn, self.text_height, textColor, self.text2)

    def updateLoc(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.outline.x = x-4
        self.outline.y = y-4
        self.outline.width = width+8
        self.outline.height = height+8

        if self.selectedItem == 1:
            self.leftToggle.rect.color = self.color
            self.rightToggle.rect.color = self.highLightColor
        else:
            self.leftToggle.rect.color = self.highLightColor
            self.rightToggle.rect.color = self.color

        self.leftToggle.updateLoc(x,y,width//2,height)
        self.rightToggle.updateLoc(x+width//2,y,width//2,height)
        
    def draw(self,outline = None):
        #Call this method to draw the button on the screen
        if outline or self.over == True:
            self.outline.draw()

        self.leftToggle.draw()
        self.rightToggle.draw()

    def isOver(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
            
        return False

    def toggleSelected(self):
        if self.selectedItem == 1:
            self.selectedItem = 0
        else:
            self.selectedItem = 1



class listBox():
    def __init__ (self, colorIn, text_height, textColor):
        self.color = colorIn
        self.text_height = text_height
        self.textColor = textColor
        self.over = False
        self.listOfObjects = []
        self.highlightedNum = 1
        self.currentStart = 0
        self.highlightcolor = [185,185,185]
        self.isEditingSelected = False

        self.x = 1
        self.y = 1
        self.width = 1
        self.height = 1

        self.rect = shapes.Rectangle(1,1,1,1, color=colorIn)

    def updateLoc(self,x,y,width,height, updateList):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect.x = x
        self.rect.y = y
        self.rect.width = width
        self.rect.height = height

        self.listOfObjects = updateList
        
    def draw(self,outline = None):
        #Call this method to draw the button on the screen
        self.rect.draw()

        if self.listOfObjects != []:
            if type(self.listOfObjects) == list:
                for x in range(self.currentStart, len(self.listOfObjects)):
                    yValueRect = self.y + self.height - (self.text_height+10)- ((self.text_height+10)*(x-self.currentStart))
                    if yValueRect > self.y:
                        if self.highlightedNum == x:
                            currentBox = shapes.Rectangle(self.x, yValueRect,self.width,self.text_height+10, color=self.highlightcolor)
                            currentBox.draw()
                        text = self.listOfObjects[x]
                        current = pyglet.text.Label(text, font_size = self.text_height, color=self.textColor, font_name='Arial',anchor_x='left', anchor_y='top')
                        current.x = self.x+5
                        current.y = self.y + self.height - ((self.text_height+10)*(x-self.currentStart))
                        current.draw()


    def isOver(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
            
        return False

    def changeSelected(self, x, y):
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                mousey = y - self.y
                self.highlightedNum = self.currentStart + ((self.height-mousey)//(self.text_height+10))



class layoutScreen():
    def __init__(self):
        #-----Create Button Objects-----#
        self.modelTabButton = Button([150,150,150], 12, [255,255,255,255], "Model")

        self.modelListBox= listBox([255,255,255], 16, [0,0,0,255])
        self.settingsListBox= listBox([255,255,255], 16, [0,0,0,255])

    def runTime(self, width, height):
        #-----Update all Objects-----#
        self.modelTabButton.updateLoc(5,(height-80),60,20)

        self.modelListBox.updateLoc(5,(height - 85)-(height-85)/2 + 10,300,(height - 85)/2-10, ["A","B","C","D","A","B","C","D","A","B","C","D","A","B","C","D","A","B","C","D",])
        self.settingsListBox.updateLoc(5,5,300,(height - 85)/2, ["A","B","C","D"])
        #-----Draw All Objects-----#
        self.modelTabButton.draw()

        self.modelListBox.draw()
        self.settingsListBox.draw()

    def mouseMotion(self, x, y,):
        self.modelTabButton.over = self.modelTabButton.isOver(x, y)

    def actionInput(self, mouseX, mouseY, mouseButton, modifiers):
        #left mouse Button Pressed
        if mouseButton == 1:
            if self.modelTabButton.isOver(mouseX,mouseY):
                print("modelTabButton")

            self.modelListBox.changeSelected(mouseX, mouseY)

        #Right mouse Button Pressed
        if mouseButton == 4 or (mouseButton==1 and (modifiers==18 or modifiers == 20)):#Right Click or alt/ctr Left Click
            pass







class displayScreen():
    def __init__(self):
        self.quickButtonOBJList = [[],[],[],[],[],[],[]]#height, just add more brackets for rows
        matrixWidth = 7 #number of columns across
        for x in range(matrixWidth):
            for y in range(len(self.quickButtonOBJList)):
                self.quickButtonOBJList[x].append(Button([150,150,150], 15, [255,255,255,255], "["+str(x)+", "+str(y)+"]" ))

        #-----Create Button Objects-----#
        self.highLightRect = Button([255,255,255], 15, [255,255,255,255], "")

        self.currentHighlistkey = [-1,-1]

        self.buttonVSInstant = toggleButton([125,125,125],[50,50,250], 15, [255,255,255,255], 'Key', 'Instant')

    def runTime(self, width, height):
        #-----Update all Objects-----#
        x = 0
        for col in self.quickButtonOBJList:
            for rowObj in range(len(col)):
                col[rowObj].updateLoc(10+x*10+x*125,(height-165)-rowObj*10-rowObj*100,125,100)
            x = x+1

        #-----Draw All Objects-----#
        rowHighlight = self.currentHighlistkey[0]
        colHighlight = self.currentHighlistkey[1]

        if rowHighlight > -1 and colHighlight == -1:
            self.highLightRect.updateLoc(0,(height-165)-5 -rowHighlight*110,135*7 +10,110)
            self.highLightRect.draw()

        if rowHighlight > -1 and colHighlight > -1:
            self.highLightRect.updateLoc(5+colHighlight*135 ,(height-165)-5 -rowHighlight*110,135,110)
            self.highLightRect.draw()

        for x in self.quickButtonOBJList:
            for obj in x:
                obj.draw()

        self.buttonVSInstant.updateLoc(965,height-95,200,30)
        self.buttonVSInstant.draw()

    def mouseMotion(self, x, y,):
        self.buttonVSInstant.over = self.buttonVSInstant.isOver(x, y)

        for i in self.quickButtonOBJList:
            for obj in i:
                obj.over = obj.isOver(x,y)

    def actionInput(self, mouseX, mouseY, mouseButton, modifiers):
        #left mouse Button Pressed
        if mouseButton == 1:
            if self.buttonVSInstant.isOver(mouseX,mouseY):
                self.buttonVSInstant.toggleSelected()

            for x in range(len(self.quickButtonOBJList)):
                for r in range(len(self.quickButtonOBJList[x])):
                    if self.quickButtonOBJList[x][r].isOver(mouseX,mouseY):
                        print("testButton[",x,"][",r, "] Left")
                        

        #Right mouse Button Pressed
        if mouseButton == 4 or (mouseButton==1 and (modifiers==18 or modifiers == 20)):#Right Click or alt/ctr Left Click
            for x in range(len(self.quickButtonOBJList)):
                for r in range(len(self.quickButtonOBJList[x])):
                    if self.quickButtonOBJList[x][r].isOver(mouseX,mouseY):
                        print("testButton[",x,"][",r, "] Right")

    def keysPress(self, symbol):
        lastvalueHigh = self.currentHighlistkey[0]

        if symbol == 96:
            if self.buttonVSInstant.selectedItem == 0:
                print('` - Cue')
                self.sendAction(self.currentHighlistkey[1], self.currentHighlistkey[0])
                #####self.actionReset()

        if symbol == key.F1:
            if self.currentHighlistkey[0] == 0:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 0
        elif symbol == key.F2:
            if self.currentHighlistkey[0] == 1:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 1
        elif symbol == key.F3:
            if self.currentHighlistkey[0] == 2:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 2
        elif symbol == key.F4:
            if self.currentHighlistkey[0] == 3:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 3
        elif symbol == key.F5:
            if self.currentHighlistkey[0] == 4:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 4
        elif symbol == key.F6:
            if self.currentHighlistkey[0] == 5:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 5
        elif symbol == key.F7:
            if self.currentHighlistkey[0] == 6:
                self.currentHighlistkey[0] = -1
                self.currentHighlistkey[1] = -1
            else:
                self.currentHighlistkey[0] = 6

        validNumPress = False
        if symbol == key._1 or symbol == key.NUM_1:
            self.currentHighlistkey[1] = 0
            validNumPress = True
        if symbol == key._2 or symbol == key.NUM_2:
            self.currentHighlistkey[1] = 1
            validNumPress = True
        if symbol == key._3 or symbol == key.NUM_3:
            self.currentHighlistkey[1] = 2
            validNumPress = True
        if symbol == key._4 or symbol == key.NUM_4:
            self.currentHighlistkey[1] = 3
            validNumPress = True
        if symbol == key._5 or symbol == key.NUM_5:
            self.currentHighlistkey[1] = 4
            validNumPress = True
        if symbol == key._6 or symbol == key.NUM_6:
            self.currentHighlistkey[1] = 5
            validNumPress = True
        if symbol == key._7 or symbol == key.NUM_7:
            self.currentHighlistkey[1] = 6
            validNumPress = True

        if lastvalueHigh != self.currentHighlistkey[0]:
            self.currentHighlistkey[1] = -1

        if self.currentHighlistkey[0] > -1 and validNumPress == True:#Says Key of Value was pressed
            if self.buttonVSInstant.selectedItem == 1:
                self.sendAction(self.currentHighlistkey[0], self.currentHighlistkey[1])

    def sendAction(self, x,y):
        print(x,y)

    def actionReset(self,):
        self.currentHighlistkey = [-1,-1]
        

