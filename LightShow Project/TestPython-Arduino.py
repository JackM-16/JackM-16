import time
import SerialCsvTest 
import csv
import LightGuiDef

f = open('LightShow.txt', 'r')

reader = csv.reader(f)

testDict = {}

for row in reader:
    timesRepeat = int(row[1])
    R = 0
    FinalList = [int(row[1])]
    X4 = 2
    while (R < timesRepeat):
        Dictlist = []
        Dictlist.append(row[X4])
        X4 = X4 + 1
        Dictlist.append(row[X4])
        X4 = X4 + 1
        Dictlist.append(row[X4])
        X4 = X4 + 1
        Dictlist.append(row[X4])
        X4 = X4 + 1
        Dictlist.append(row[X4])
        X4 = X4 + 1

        FinalList.append(Dictlist)
    
        R = R +1
    
    testDict[float(row[0])] = FinalList
print(testDict)

timeRepeat = 0
x = True
then = time.time()

while (x == True):
    now = time.time() #Time after it finished
    timerCount = round(now-then, 2)

    if timerCount in testDict:
        
        itemNumber = testDict[timerCount]
        print(timerCount)
        x4 = 1
        i = 0
        while (i < itemNumber[timeRepeat]):
            i = i + 1
            pinNumber = itemNumber[x4][1]
            R = itemNumber[x4][2]
            G = itemNumber[x4][3]
            B = itemNumber[x4][4]
            SerialCsvTest.sendPixel(pinNumber,R,G,B)
            
            x4 = 1 + x4
#while True:
    #SerialCsvTest.usb_downLeft()
#    asd = input("enter a  number")
#    SerialCsvTest.usb_downReft(asd, "Hello")
