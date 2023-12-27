from transformers import pipeline
from datasets import load_dataset
import soundfile as sf
import torch

# works great
synthesiser = pipeline("text-to-speech", "microsoft/speecht5_tts")

embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
speaker_embedding = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)
# You can replace this embedding with your own as well.

speech = synthesiser("Hello, my name is diana, this works very well!", forward_params={"speaker_embeddings": speaker_embedding})

sf.write("hello.wav", speech["audio"], samplerate=speech["sampling_rate"])

