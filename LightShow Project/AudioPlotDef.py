import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import librosa as lr
import time
import pygame
from pygame.locals import *

import tkinter
from tkinter import *
from tkinter import filedialog, Text

def addFile():
    root = Tk()
    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("WavForm", "*.wav"), ("all files", "*.*")))
    root.destroy()
    return(filename)

class audioWave():
    def __init__(self,audioFile, startX, startY):
        self.audioFile = audioFile
        self.x = startX
        self.y = startY
        self.audio, self.sfreq = lr.load(self.audioFile)
        self.time = np.arange(0, len(self.audio)) / self.sfreq
        self.StartTimeline = (0,2)

        self.length = 1 
        self.width = 1
        
        self.LinePos = (startX, startY)
        self.lineGraphpos = self.StartTimeline[0]
        self.lastLength = 0

    def updateFile(self, newFile):
        self.audioFile = newFile
        self.audio, self.sfreq = lr.load(self.audioFile)
        self.time = np.arange(0, len(self.audio)) / self.sfreq
        print("done")

    def click(self, pos, win, length):
        if pos[0] >= self.x and pos[0] <= self.x + length:
            self.LinePos = pos
            #roundedNumber = (round((pos[0] - self.x) / length,2) + self.StartTimeline[0])
            
            roundedNumber = round(((pos[0] - self.x) / length) * (self.StartTimeline[1] - self.StartTimeline[0]),2) + self.StartTimeline[0]
            self.lineGraphpos = round(roundedNumber,2)
        return(self.getGraphNumber())

    def getGraphNumber(self):
        return(self.lineGraphpos)
    
    def changeGraphNumber(self,ChangeAmount, length):
        self.lineGraphpos = round(self.lineGraphpos + ChangeAmount, 2)
        calculate = (((self.lineGraphpos - self.StartTimeline[0]) / (self.StartTimeline[1] - self.StartTimeline[0]))* length) + self.x
        self.LinePos = (int(calculate) ,self.y)
            
    def drawLocationLine(self, win):
        pygame.draw.line(win,(0,0,0),(self.LinePos[0],self.y), (self.LinePos[0],self.y + self.width), 2)

    def updateLocation(self, newX, newY):
        self.x = newX
        self.y = newY
        
    def draw(self, screen, length, width):
        self.length = int(length)
        self.width = int(width)

        self.StartTimeline = (self.StartTimeline[0], self.StartTimeline[0] + (round(self.length/25,0) / 5))
    
    
        if self.lastLength != length:
            
            fig, ax = plt.subplots(figsize=(length/100, width/100))
            ax.plot(self.time, self.audio)

            ax.set_xlim(self.StartTimeline)
            ax.set_ylim(-0.31, 0.31)
            plt.subplots_adjust(left= 0.001, bottom=0.08, right=0.999, top=0.98)

            self.canvas = agg.FigureCanvasAgg(fig)
            self.canvas.draw()
            self.renderer = self.canvas.get_renderer()
            self.raw_data = self.renderer.tostring_rgb()

        self.lastLength = length

        size = self.canvas.get_width_height()

        time.sleep(.025)

        surf = pygame.image.fromstring(self.raw_data, size, "RGB")
        screen.blit(surf, (self.x,self.y))
        plt.close()

class showGraph():
    def __init__(self, dictIn, startX, startY):
        self.x = startX
        self.y = startY
        self.plotY = []
        self.plotX = dictIn.keys()
        self.StartTimeline = (0,2)

        for i in range(len(dictIn)):
            self.plotY.append(0)

        self.length = 1 
        self.width = 1
        
        self.LinePos = (startX, startY)
        self.lineGraphpos = self.StartTimeline[0]
        self.lastLength = 0

    def updateList(self, newDict):
        self.plotX = newDict.keys()
        self.plotY = []
        for i in range(len(self.plotX)):
            self.plotY.append(0)

        
    def click(self, pos, win, length):
        if pos[0] >= self.x and pos[0] <= self.x + length:
            self.LinePos = pos
            #roundedNumber = (round((pos[0] - self.x) / length,2) + self.StartTimeline[0])
            
            roundedNumber = round(((pos[0] - self.x) / length) * (self.StartTimeline[1] - self.StartTimeline[0]),2) + self.StartTimeline[0]
            self.lineGraphpos = round(roundedNumber,2)
        return(self.getGraphNumber())

    def changeGraphNumber(self,ChangeAmount, length):
        self.lineGraphpos = round(self.lineGraphpos + ChangeAmount, 2)
        calculate = (((self.lineGraphpos - self.StartTimeline[0]) / (self.StartTimeline[1] - self.StartTimeline[0]))* length) + self.x
        self.LinePos = (int(calculate) ,self.y)
            
        
    def getGraphNumber(self):
        return(self.lineGraphpos)

    def drawLocationLine(self, win):
        pygame.draw.line(win,(0,0,0),(self.LinePos[0],self.y), (self.LinePos[0],self.y + self.width), 2)

    def updateLocation(self, newX, newY, newDict):
        self.x = newX
        self.y = newY
        self.updateList(newDict)
        
    def draw(self, screen, length, width, byPass = False):
        self.length = int(length)
        self.width = int(width)

        self.StartTimeline = (self.StartTimeline[0], self.StartTimeline[0] + (round(self.length/25,0) / 5))
    
        if self.lastLength != length or byPass == True:
            
            fig, ax = plt.subplots(figsize=(length/100, width/100))
            ax.scatter(self.plotX, self.plotY)

            ax.set_xlim(self.StartTimeline)
            #ax.set_ylim(-0.31, 0.31)
            plt.subplots_adjust(left= 0.001, bottom=0.08, right=.999, top=0.98)

            self.canvas = agg.FigureCanvasAgg(fig)
            self.canvas.draw()
            self.renderer = self.canvas.get_renderer()
            self.raw_data = self.renderer.tostring_rgb()

        self.lastLength = length

        size = self.canvas.get_width_height()

        surf = pygame.image.fromstring(self.raw_data, size, "RGB")
        screen.blit(surf, (self.x,self.y))
        plt.close()





class audioWavePlot():
    def __init__(self,audioFile):
        self.audioFile = audioFile
        self.audio, self.sfreq = lr.load(self.audioFile)
        self.time = np.arange(0, len(self.audio)) / self.sfreq

        self.x = 0
        self.y = 0
        self.width = 1 
        self.height = 1
        self.StartTimeline = [0,225]
        
        self.lastwidth = 0
        self.needUpdate = True

        self.lastXValue = self.time[-1]
        self.StartTimeline = [0,self.lastXValue+20]
        self.increment = 25
        self.lineDrawTime = 10
        

    def updateLoc(self, x, y, length, width):
        self.x = x
        self.y = y + 30
        self.width = int(length)
        self.height = int(width - 30)

    def clampZoom(self,newValue,):
        finalReturn = newValue
        if newValue > 600:
            finalReturn = 600
        if newValue < self.StartTimeline[0] + 10:
            finalReturn = self.StartTimeline[0] + 10
        return(finalReturn)

    def clampLeftRight(self,newValue,):
        finalReturn = newValue
        if newValue > self.lastXValue:
            finalReturn = self.lastXValue
        if newValue < 0:
            finalReturn = 0
        return(finalReturn)

    def clampIncrement(self,newValue,):
        finalReturn = newValue
        if newValue > 50:
            finalReturn = 50
        if newValue < 1:
            finalReturn = 1
        return(finalReturn)
        
    def getTimeSelected(self):
        textFirst = self.lineDrawTime
        if textFirst/60 >= 1:
            textFirst = str(int(int(textFirst/60))) + ":" + str(int(int(textFirst%60))) + ":" + str(int(  100*( textFirst%1)  ))
        else:
            textFirst =  "0:" + str(int(int(textFirst%60))) + ":" + str(int(  100*( textFirst%1)  ))
        return(textFirst)


        
    def draw(self, screen):
        try:
            if self.lastwidth != self.width or self.needUpdate == True:
                
                fig, ax = plt.subplots(figsize=(self.width/100, self.height/100))
                ax.plot(self.time, self.audio)

                ax.set_xlim(self.StartTimeline[0], self.StartTimeline[1])
                ax.set_ylim(-1.5, 1.5)
                plt.subplots_adjust(left= 0.001, bottom=0.08, right=0.999, top=0.98)
                plt.subplots_adjust(left= 0, bottom=0, right=1, top=1)

                self.canvas = agg.FigureCanvasAgg(fig)
                self.canvas.draw()
                self.renderer = self.canvas.get_renderer()
                self.raw_data = self.renderer.tostring_rgb()
                self.needUpdate = False

            self.lastwidth = self.width

            size = self.canvas.get_width_height()

            surf = pygame.image.fromstring(self.raw_data, size, "RGB")
            screen.blit(surf, (self.x, self.y))
            plt.close('all')
            plt.clf()
        except:
            print("err")
            plt.close('all')
            plt.clf()

        font = pygame.font.SysFont('arial', 14)
        
        textFirst = self.StartTimeline[0]
        if textFirst/60 >= 1:
            textFirst = str(int(int(textFirst/60))) + ":" + str(int(int(textFirst%60))) + ":" + str(int(  100*( textFirst%1)  ))
        else:
            textFirst =  "0:" + str(int(int(textFirst%60))) + ":" + str(int(  100*( textFirst%1)  ))
        text = font.render(textFirst, 1, ([0,0,0]))
        screen.blit(text, (self.x-1, self.y-30))
        
        text = font.render("|", 1, ([0,0,0]))
        screen.blit(text, (self.x-1, self.y-15))

        changeTime = self.StartTimeline[1]
        endTime = str(int(int(changeTime/60))) + ":" + str(int(int(changeTime%60))) + ":" + str(int(  100*( changeTime%1)  ))
        text = font.render(endTime, 1, ([0,0,0]))
        screen.blit(text, (self.x+self.width-text.get_width()-1, self.y-30))
        
        text = font.render("|", 1, ([0,0,0]))
        screen.blit(text, (self.x+self.width-1, self.y-15))
        for x in range(1,20):
            screen.blit(text, (self.x+(self.width/20)*x -1, self.y-15))
            if x %2 == 0:
                textString = self.StartTimeline[0] + ((self.StartTimeline[1]-self.StartTimeline[0])/20) * x
                if textString/60 >= 1:
                    textString = str(int(int(textString/60))) + ":" + str(int(int(textString%60))) + ":" + str(int(  100*( textString%1)  ))
                else:
                    textString =  "0:" + str(int(int(textString%60))) + ":" + str(int(  100*( textString%1)  ))
                text2 = font.render(str(textString), 1, ([0,0,0]))
                screen.blit(text2, (self.x+(self.width/20)*x -1-text2.get_width()/2, self.y-30))

        ###Draw line Time selected###
        if self.lineDrawTime <= self.StartTimeline[1] and self.lineDrawTime >= self.StartTimeline[0]:
            drawStartPosition = (self.x + (self.width/(self.StartTimeline[1]-self.StartTimeline[0])) * (self.lineDrawTime-self.StartTimeline[0]),self.y)
            drawEndPosition = (self.x + (self.width/(self.StartTimeline[1]-self.StartTimeline[0])) * (self.lineDrawTime-self.StartTimeline[0]),self.y+self.height)
            
            pygame.draw.line(screen,(0,0,0),(drawStartPosition), (drawEndPosition), 3)



        

    def eventHandler(self, event):
        pos = pygame.mouse.get_pos()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.lineDrawTime = self.StartTimeline[0] + ((pos[0] - self.x)/self.width)*(self.StartTimeline[1]-self.StartTimeline[0])
                    
                    if event.button == 2:
                        print("middle")
                        self.StartTimeline[1] = 10
                    if event.button == 4:
                        print("up")
                        self.StartTimeline[1] = self.clampZoom(self.StartTimeline[1] - self.increment)
                        self.needUpdate = True
                    elif event.button == 5:
                        print("down")
                        self.StartTimeline[1] = self.clampZoom(self.StartTimeline[1] + self.increment)
                        self.needUpdate = True
                    plt.close('all')
                    plt.clf()
                    
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    self.StartTimeline[0] = self.clampLeftRight(self.StartTimeline[0] - self.increment)
                    self.StartTimeline[1] = self.clampZoom(self.StartTimeline[1] - self.increment)
                    self.needUpdate = True
                if keys[pygame.K_RIGHT]:
                    self.StartTimeline[0] = self.clampLeftRight(self.StartTimeline[0] + self.increment)
                    self.StartTimeline[1] = self.clampZoom(self.StartTimeline[1] + self.increment)
                    self.needUpdate = True
                if keys[pygame.K_UP]:
                    self.increment = self.clampIncrement(self.increment+5)
                if keys[pygame.K_DOWN]:
                    self.increment = self.clampIncrement(self.increment-5)
                    























            
                    
                


