import matplotlib.pyplot as plt
import numpy as np
import wave

class imagePlotter():
    def __init__(self, audioFile,saveLocation):
        self.audioFile = wave.open(audioFile, 'rb')
        self.fileLocationSave = saveLocation
        self.maxlength = 0
        self.createWave()
    
    def createWave(self,):
        sampleFreq = self.audioFile.getframerate()
        n_samples = self.audioFile.getnframes()

        audioTime = n_samples / sampleFreq
        self.maxlength = audioTime

        signalWave = self.audioFile.readframes(n_samples) 
        signalArray = np.frombuffer(signalWave, dtype=np.int16) 
        self.lChannel = signalArray[0::2] 
        self.times = np.linspace(0, audioTime, num=n_samples) 
        self.updateGraph(0,audioTime,15.7)

    def updateGraph(self,start, end, figWidth):
        plt.figure(figsize=(figWidth, 1)) 
        plt.plot(self.times, self.lChannel)       
        plt.xlim(start, end)
        plt.ylim(-35000, 35000)
        ##This removes All White Space##plt.sublots_adjust(left= 0.0, bottom=0.0, right=1, top=1)
        plt.subplots_adjust(left= 0.0,bottom=0.5 , right=1, top=1)#Just for testing
        plt.savefig(self.fileLocationSave)
        plt.close('all')

def changeTimeType(time):
        if time/60 >= 1:
            time = str(int(int(time/60))) + ":" + str(int(int(time%60))) + ":" + str(int(  100*( time%1)  ))
        else:
            time =  "0:" + str(int(int(time%60))) + ":" + str(int(  100*( time%1)  ))
        return(time)