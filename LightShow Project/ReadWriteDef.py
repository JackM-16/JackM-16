import csv

def read(filename):
    f = open(filename, 'r')
    reader = csv.reader(f)
    dictName = {}
    
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
    
        dictName[float(row[0])] = FinalList
    return dictName

def write(filename,testDict):
    saveFile = open(filename, 'w')
    for i in testDict:
        saveFile.write(str(i)+ ",")
        saveFile.write(str(testDict[i][0])+ ",")#times repeat
        x=0
        while (x < testDict[i][0]):
            x = x+1
            saveFile.write((str(testDict[i][x][0]).strip("[]''")) + ","+ (str(testDict[i][x][1]).strip("[]''")) + ","+ (str(testDict[i][x][2]).strip("[]''")) + ","+ (str(testDict[i][x][3]).strip("[]''")) + ","+ (str(testDict[i][x][4]).strip("[]''"))+ ",")
        saveFile.write("\n")
    saveFile.close()
def addPixel(testDict,time,pin,R,G,B):
    if time in testDict:
        timesRepeat = testDict[time][0]
        for repeatX in range(timesRepeat - 1):
            if testDict[time][repeatX + 1][1] == str(pin):
                del testDict[time][repeatX + 1]
                testDict[time][0] = testDict[time][0] - 1
                
        testDict[time][0] = testDict[time][0] + 1
        testDict[time].append(["Pixel",updateDigitsNumber(pin, 3),updateDigitsNumber(R, 3),updateDigitsNumber(G, 3),updateDigitsNumber(B, 3)])
    else: 
        #testDict[time] = [1,["Pixel",str(pin),str(R),str(G),str(B)]]
        testDict[time] = [1,["Pixel",updateDigitsNumber(pin, 3),updateDigitsNumber(R, 3),updateDigitsNumber(G, 3),updateDigitsNumber(B, 3)]]

def updateDigitsNumber(number, digitsAmount):
    strNum = str(number)
    if len(strNum) < digitsAmount:
        for i in range(digitsAmount - len(strNum)):
            strNum = "0" + strNum
    return strNum
    


    
