import librosa
import sys

def load_audio(fname):
    a, _ = librosa.load(fname, sr=16000)
    return a

audio_path = "D:\Download\sample1.flac" 

SAMPLING_RATE = 16000
duration = len(load_audio(audio_path))/SAMPLING_RATE
print("Audio duration is: %2.2f seconds" % duration, file=sys.stderr)
