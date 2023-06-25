import serial
import time

################# '1'.encode("ascii") ##################Test For base64 encoding to test with arduino text


openPort = False
try:
    #usbCom = serial.Serial('COM5', 16500)
    usbCom = serial.Serial('COM5', 19200)
    usbCom.close()
    usbCom.open()
    openPort = True
    print("connected")
except:
    print("No Pixel")
    openPort = False

def usb_test():
    global code1
    code1 = 2
    usbCom.write('1'.encode())
    time.sleep(1)
    print('sent test code')
    while code1 == 2:
        msg = usbCom.read(usbCom.inWaiting()) # read all characters in buffer
        msg = str(msg)
        message = msg.strip(" \ n r b ' ")
        print (message)
        if message == '3':
            print ("The message was recieved")
            code1 = 4
        time.sleep(1)

def sendPixel():
    usbCom.write('1'.encode())
    print('sent')
    
def usb_downLeft():
    usbCom.write('2'.encode())
    time.sleep(1)
    usbCom.write('1'.encode())
    msg = usbCom.read(usbCom.inWaiting()) # read all characters in buffer
    msg = str(msg)
    message = msg.strip("\nrb'")
    print (message)

def usb_downReft(hello,goodbye):
    usbCom.write(hello.encode())
    time.sleep(1)
    msg = usbCom.read(usbCom.inWaiting()) # read all characters in buffer
    msg = str(msg)
    message = msg.strip(" \ n r b ' ")
    print ("\n" + message)
    print (goodbye)

def sendPixel(pinNum,r,g,b):
    if openPort == True:
       #usbCom.write('1'.encode())
        usbCom.write(pinNum.encode() + r.encode() + g.encode() + b.encode())
        #usbCom.write(r.encode())
        #usbCom.write(g.encode())
        #usbCom.write(b.encode())

        
    #time.sleep(.05)
    #msg = usbCom.read(usbCom.inWaiting()) # read all characters in buffer
    #msg = str(msg)
    #message = msg.strip(" \ n r b ' ")
    #print (message.strip(" \ n r b '"))
    
    



