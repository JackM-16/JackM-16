import serial
import time

openPort = False
try:
    #usbCom = serial.Serial('COM5', 16500)
    usbCom = serial.Serial('COM3', 115200)
    usbCom.close()
    usbCom.open()
    openPort = True
    print("connected")
except:
    print("No Pixel")
    openPort = False



def sendPixel(pinNum,r,g,b):
    if openPort == True:
        usbCom.write(pinNum.encode('utf-8') + r.encode('utf-8') + g.encode('utf-8') + b.encode('utf-8'))
    
def updateDigitsNumber(number, digitsAmount):
    strNum = str(number)
    if len(strNum) < digitsAmount:
        for i in range(digitsAmount - len(strNum)):
            strNum = "0" + strNum
    return strNum
    

timeWait = .01
timeWait = .02
time.sleep(2)
for x in range(2):
    for x in range(10):
        usbCom.write("000255255255".encode())
        usbCom.write("001255255255".encode())
        usbCom.write("002255255255".encode())
        usbCom.write("003255255255".encode())
        usbCom.write("004255255255".encode())
        usbCom.write("005255255255".encode())
        time.sleep(timeWait)
        usbCom.write("999999999999".encode())
        time.sleep(timeWait)
        usbCom.write("000000000000".encode())
        usbCom.write("001000000000".encode())
        usbCom.write("002000000000".encode())
        usbCom.write("003000000000".encode())
        usbCom.write("004000000000".encode())
        usbCom.write("005000000000".encode())
        time.sleep(timeWait)
        usbCom.write("999999999999".encode())
        time.sleep(timeWait)

    ##for x in range(10):
        ##for x in range(150):
            ##usbCom.write((updateDigitsNumber(x,3)+"255255255").encode())
        ##usbCom.write("999999999999".encode())
        ##time.sleep(.01)
        ##for x in range(150):
            ##usbCom.write((updateDigitsNumber(x,3)+"000000000").encode())
        ##usbCom.write("999999999999".encode())
        ##time.sleep(.01)
    
    print(True)


    for x in range(10):
        usbCom.write("000255255255001255255255002255255255003255255255004255255255005255255255006255255255007255255255008255255255009255255255010255255255011255255255012255255255013255255255014255255255015255255255016255255255017255255255018255255255019255255255020255255255021255255255022255255255023255255255024255255255999999999999".encode())
        time.sleep(timeWait)
        usbCom.write("000000000000001000000000002000000000003000000000004000000000005000000000006000000000007000000000008000000000009000000000010000000000011000000000012000000000013000000000014000000000015000000000016000000000017000000000018000000000019000000000020000000000021000000000022000000000023000000000024000000000999999999999".encode())
        time.sleep(timeWait)


strmain = ""
for x in range(150):
    strmain = strmain + (updateDigitsNumber(x,3)+"050000000")
strmain = strmain + "999999999999"

strmainoff = ""
for x in range(150):
    strmainoff = strmainoff + (updateDigitsNumber(x,3)+"000000000")
strmainoff = strmainoff + "999999999999"

for x in range(10):
    usbCom.write(strmain.encode())
    time.sleep(timeWait-.01)
    usbCom.write(strmainoff.encode())
    time.sleep(.5)

