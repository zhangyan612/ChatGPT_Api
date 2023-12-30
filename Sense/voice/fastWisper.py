from faster_whisper import WhisperModel

model_size = "large-v3"

# works on cpu
# for gpu
# Purfview's whisper-standalone-win provides the required NVIDIA libraries for Windows & Linux in a single archive. Decompress the archive and place the libraries in a directory included in the PATH.



# Run on GPU with FP16
# model = WhisperModel(model_size, device="cuda", compute_type="float16")

# or run on GPU with INT8
# model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
# or run on CPU with INT8
model = WhisperModel(model_size, device="cpu", compute_type="int8")
wav_file_path = "D:\Download\sample1.flac"

segments, info = model.transcribe(wav_file_path, beam_size=5)

print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
