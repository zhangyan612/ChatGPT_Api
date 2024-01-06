from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torchaudio
import sounddevice as sd
import numpy as np

# wisper works but slow
# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
model.config.forced_decoder_ids = None

# Record audio from the microphone
print("recording...............")

duration = 10  # seconds
fs = 16000
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
sd.wait()

# Convert the audio to the right format
input_audio = np.squeeze(myrecording)
print("recording Done")

# Tokenize the audio and convert it to input features
input_features = processor(input_audio, return_tensors="pt").input_features

# generate token ids
predicted_ids = model.generate(input_features)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

print(transcription)
