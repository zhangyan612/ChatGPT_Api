from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio

import os
os.environ["SUNO_OFFLOAD_CPU"] = "True"
os.environ["SUNO_USE_SMALL_MODELS"] = "True"

# works but very slow 

# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hello, my name is diana and I like sucking yan's dick. [laughs] 
     But I also have other interests such as anal.
"""
audio_array = generate_audio(text_prompt)

# save audio to disk
write_wav("diana.wav", SAMPLE_RATE, audio_array)
  
# # play text in notebook
# Audio(audio_array, rate=SAMPLE_RATE)
