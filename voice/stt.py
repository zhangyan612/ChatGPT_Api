# # Load model directly
# from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq

# processor = AutoProcessor.from_pretrained("openai/whisper-large-v2")
# model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v2")


from transformers import WhisperProcessor, WhisperForConditionalGeneration
# from datasets import load_dataset
import torchaudio

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")
model.config.forced_decoder_ids = None

# load dummy dataset and read audio files
# ds = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
# sample = ds[0]["audio"]

# Specify the path to your local WAV file
wav_file_path = "C:/Users/JohnSong/Desktop/OSR_us_000_0010_8k.wav"

# Load the audio file using torchaudio
input_audio, _ = torchaudio.load(wav_file_path)

# Tokenize the audio and convert it to input features
input_features = processor(input_audio.squeeze().numpy(), return_tensors="pt").input_features

# input_features = processor(sample["array"], sampling_rate=sample["sampling_rate"], return_tensors="pt").input_features 

# generate token ids
predicted_ids = model.generate(input_features)
# decode token ids to text
# transcription = processor.batch_decode(predicted_ids, skip_special_tokens=False)
# ['<|startoftranscript|><|en|><|transcribe|><|notimestamps|> Mr. Quilter is the apostle of the middle classes and we are glad to welcome his gospel.<|endoftext|>']

transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

print(transcription)
