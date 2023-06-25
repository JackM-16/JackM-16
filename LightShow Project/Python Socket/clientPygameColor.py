import pygame
import sys
import os
import time
import socket


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

#background/title
win.fill((225,0,0))  # Fills the screen with what ever color

pygame.display.set_caption("Simple Light Config")#caption

#-------Define Variables-------#
clock = pygame.time.Clock()
fullscreen = False


ColorSelected = [100,100,100]
 

port = 5000  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect(('127.0.0.1', port))  # connect to the server

while True:
    win.fill((lightGrey2))
    
    keys = pygame.key.get_pressed()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    
    #---Color---#
    pygame.draw.rect(win, ColorSelected, (10,5,245,55),0)
    
    #-------Get Mouse and Keys-------# 
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            client_socket.close()
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                win = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

        if keys[pygame.K_q]:
            client_socket.close()
            pygame.quit()
            sys.exit()
            
        if keys[pygame.K_ESCAPE]:
            client_socket.close()
            pygame.quit()
            sys.exit()

    for x in range(3):
        data = client_socket.recv(1024).decode('utf-8')
        print(data)
        ColorSelected[x] = int(data)
    print(ColorSelected)


    pygame.display.update()
