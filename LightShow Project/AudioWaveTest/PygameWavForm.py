import matplotlib.pyplot as plt
import numpy as np
import wave

# Load the .wav file
wav_file = wave.open('C:/Users/jtmti/Downloads/Easy Beat.wav', 'rb')

sampleFreq = wav_file.getframerate()
n_samples = wav_file.getnframes()

tAudio = n_samples / sampleFreq
print(tAudio)

signalWave = wav_file.readframes(n_samples) 
signalArray = np.frombuffer(signalWave, dtype=np.int16) 
lChannel = signalArray[0::2] 
times = np.linspace(0, n_samples/sampleFreq, num=n_samples) 

plt.figure(figsize=(15, 5)) 
plt.plot(times, lChannel)       
plt.xlim(0, tAudio)
plt.subplots_adjust(left= 0.0, bottom=0.0, right=1, top=1)
plt.savefig('C:/Users/jtmti/Documents/LightShow Project/AudioWaveTest/test.jpg')
print("done")

plt.figure(figsize=(15, 5)) 
plt.plot(times, lChannel)       
plt.xlim(7, 10)
#plt.subplots_adjust(left= 0.0, bottom=0.0, right=1, top=1)
plt.savefig('C:/Users/jtmti/Documents/LightShow Project/AudioWaveTest/test2.jpg')
print("done")

plt.figure(figsize=(15, 2.5)) 
plt.plot(times, lChannel)       
plt.xlim(7, 10)
plt.ylim(-35000, 35000)
#plt.subplots_adjust(left= 0.0, bottom=0.0, right=1, top=1)
plt.savefig('C:/Users/jtmti/Documents/LightShow Project/AudioWaveTest/test3.jpg')

print("done")





