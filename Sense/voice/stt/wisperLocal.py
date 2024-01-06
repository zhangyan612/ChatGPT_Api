from transformers import WhisperProcessor, WhisperForConditionalGeneration
from datasets import load_dataset


# pip install librosa 
# pip install soundfile

# Success local speech recognition

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
model.config.forced_decoder_ids = None

# load dummy dataset and read audio files
ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = ds[0]["audio"]
input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features 

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
# transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)
print(transcription)