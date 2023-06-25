import time

class baseEffect:
    def __init__(self,nameGiven):
        self.effectName = nameGiven
        self.startTime = 0.0
        self.endTime = 0.0
        self.selected = False
  
    def getData(self,screen_w,screen_h):
        return ({"Name":str(self.name),
                "Start Time":str( self.startTime),
                })

    def updateData(self, newvalue, index, screen_w, screen_h):
        if index==0:
            self.name = newvalue
        elif index==1:
            self.numLights = int(newvalue)

    def getType(self):
        return("effect")

    def draw(self,win,screen_w,screen_h,active=False, pixelSizeOverride = 0):
        pass

class onOffEffect(baseEffect):
    def __init__(self, color, etc):
        super().__init__("On Off")

    def printName(self):
        return super().printName() + str(self.start)
    

print("start-LightGUIEffect")
testInit = onOffEffect("red", 10)

#print(testInit.printName())