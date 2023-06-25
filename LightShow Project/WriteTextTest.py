import time
import csv
import ReadWriteDef
import SerialCsvTest 

testDict = ReadWriteDef.read('writeTest.txt')

print(testDict[2.5][1])
testDict[11] = [1,["Test","123","123","123","asd"]]
while True:
    time = input("enter the time")
    pin = input("enter the pin")
    r = input("enter the r")
    g = input("enter the g")
    b = input("enter the b") 

    ReadWriteDef.addPixel(testDict,int(time),pin,r,g,b)
    SerialCsvTest.sendPixel(pin,r,g,b )
    ReadWriteDef.write('writeTest.txt', testDict)


