import SerialCsvTest as PixelWrite
import ReadWriteDef as NumUpdate
import time

time.sleep(1)
PixelWrite.sendPixel('009','255','200','050')
PixelWrite.sendPixel('027','255','200','050')
PixelWrite.sendPixel('031','255','200','050')
PixelWrite.sendPixel('049','255','200','050')
PixelWrite.sendPixel('999','999','999','999')


while True:
    num = input(":")
    if num == "r":
        top = int(input("start"))
        end = int(input("end"))
        for x in range(top,end+1):
            val = str(NumUpdate.updateDigitsNumber(x,3))
            PixelWrite.sendPixel(val,'255','200','050')
        PixelWrite.sendPixel('999','999','999','999')


    else:    
        PixelWrite.sendPixel(str(num),'255','255','255')
        PixelWrite.sendPixel('999','999','999','999')

