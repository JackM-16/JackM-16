from socket import *
import time

address= ( '192.168.1.99', 5000) #define server IP and port
client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
client_socket.settimeout(1) #Only wait 1 second for a response


def calPixelVal(pin,r,g,b):
    #PinCalulations
    if (pin%170) == 0:
        finalPin = str(chr(33+(pin//170))) + str(chr(33))  + str(chr(33))
    else:
        sepVal = pin%170
        if sepVal > 85:
            sepOne = sepVal - 85
            sepTwo = 85
        else: 
            sepOne = 0
            sepTwo = sepVal
        finalPin = str(chr(33+(pin//170))) + str(chr(33+sepOne))  + str(chr(33+sepTwo))
    #Color Calculations
    finalR = str(chr(33+r//3))
    finalG = str(chr(33+g//3))
    finalB = str(chr(33+b//3))
    return(finalPin+finalR+finalG+finalB)


brightWhiteList = []
for x in range(0,200,4):
    brightWhiteList.append(calPixelVal(x,50,50,50) + calPixelVal(x+1,50,50,50)+calPixelVal(x+2,50,50,50)+calPixelVal(x+3,50,50,50))

for x in range(len(brightWhiteList)):
    data = brightWhiteList[x].encode()
    client_socket.sendto( data, address) #Send the data request
data = ('!!!w!!').encode() #Turns On All The Lights
client_socket.sendto( data, address) #Send the data request
time.sleep(10)

data = ('!!!x!!').encode() #Turns off All the Lights
client_socket.sendto( data, address) #Send the data request
time.sleep(1)

data = calPixelVal(1,100,100,100).encode()
client_socket.sendto( data, address) #Send the data request
data = ('!!!w!!').encode()
client_socket.sendto( data, address) #Send the data request
print("On")


time.sleep(5)

redOnList = []
for x in range(0,200,4):
    redOnList.append(calPixelVal(x,50,0,0) + calPixelVal(x+1,50,0,0)+calPixelVal(x+2,50,0,0)+calPixelVal(x+3,50,0,0))

blueOnList = []
for x in range(0,200,4):
    blueOnList.append(calPixelVal(x,0,0,50) + calPixelVal(x+1,0,0,50)+calPixelVal(x+2,0,0,50)+calPixelVal(x+3,0,0,50))

#Time between max is .05
while True:
    for x in range(len(redOnList)):
        data = redOnList[x].encode()
        client_socket.sendto( data, address) #Send the data request
    data = ('!!!w!!').encode() #Turns On All The Lights
    client_socket.sendto( data, address) #Send the data request
    time.sleep(.05)
    for x in range(len(blueOnList)):
        data = blueOnList[x].encode()
        client_socket.sendto( data, address) #Send the data request
    data = ('!!!w!!').encode() #Turns On All The Lights
    client_socket.sendto( data, address) #Send the data request
    time.sleep(.05)
    data = ('!!!x!!').encode() #Turns Off All The Lights
    client_socket.sendto( data, address) #Send the data request
    time.sleep(.05)

