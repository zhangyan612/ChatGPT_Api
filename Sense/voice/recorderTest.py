import sounddevice as sd
from scipy.io.wavfile import write

# works fine, make sure recorder is not muted
fs=44100
duration=5
print("recording...............")


record_voice=sd.rec(int(duration * fs),samplerate=fs,channels=2)
sd.wait()       
write("sound.wav",fs,record_voice)
