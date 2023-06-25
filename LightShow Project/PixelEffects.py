import SerialCsvTest as PixelWrite
import ReadWriteDef as NumUpdate
import random
import time

def twinkle(numLights):
    for x in range(numLights):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'000','000','000')
    blinkPixel = random.randrange(0, numLights, 1)
    blinkPixel2 = random.randrange(0, numLights, 1)
    blinkPixel3 = random.randrange(0, numLights, 1)
    
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel,3)),'255','255','255')
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel2,3)),'255','255','255')
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel3,3)),'255','255','255')
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-A")
    time.sleep(.2)
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel,3)),'000','000','000')
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel2,3)),'000','000','000')
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel3,3)),'000','000','000')
    delay = random.randrange(1, 5)/10
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-B")
    time.sleep(delay)


def policeSplit(numLights):
    middle = numLights//2
    for x in range(middle):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'000','000','255')
        time.sleep(.001)
    for x in range(middle, numLights):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'255','000','000')
        time.sleep(.001)
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-A")
    time.sleep(.75)
    for x in range(middle):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'255','000','000')
    for x in range(middle, numLights):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'000','000','255')
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-B")
    time.sleep(.75)
        
def candyCane(numLights):
    length = 6
    for z in range(length):
        for x in range (-(-numLights//length)):
            if (x%2 == 0):
                for y in range(length):
                    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber((x*length)+y+z,3)),'050','050','050')

            else:
                for y in range(length):
                    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber((x*length)+y+z,3)),'150','000','000')
        PixelWrite.sendPixel('999','999','999','999')
        time.sleep(.75)
        
    for z in range(length):
        for x in range (-(-numLights//length)):
            if (x%2 == 0):
                for y in range(length):
                    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber((x*length)+y+z,3)),'150','000','000')

            else:
                for y in range(length):
                    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber((x*length)+y+z,3)),'050','050','050')
        PixelWrite.sendPixel('999','999','999','999')
        time.sleep(.75)


        
    

    

        
def snowSparkle(numLights):
    for x in range(numLights):
        PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(x,3)),'025','025','025')

    blinkPixel = random.randrange(0, numLights, 1)
    
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel,3)),'255','255','255')
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-A")
    time.sleep(.2)
    PixelWrite.sendPixel(str(NumUpdate.updateDigitsNumber(blinkPixel,3)),'025','025','020')
    delay = random.randrange(1, 5)/10
    PixelWrite.sendPixel('999','999','999','999')
    print("Sent-B")
    time.sleep(delay)
