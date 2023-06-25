import SerialCsvTest as PixelWrite
import time
import ReadWriteDef as write

time.sleep(5)

PixelWrite.sendPixel('009','100','100','100')
PixelWrite.sendPixel('027','100','100','100')
PixelWrite.sendPixel('999','999','999','999')
time.sleep(1)
print("done")


for x in range(31,50):
    PixelWrite.sendPixel(str(write.updateDigitsNumber(x,3)),'000','000','000')
    time.sleep(1.)
#for x in range(9,28):
#    PixelWrite.sendPixel(str(write.updateDigitsNumber(x,3)),'000','000','000')
PixelWrite.sendPixel('999','999','999','999')
    