 


async def async_stt() -> (str, str):
    try:
        audio_data = sd.rec(
            int(AUDIO_RECORD_TIME * AUDIO_SAMPLE_RATE),
            samplerate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
        )
        sd.wait()  # Wait until recording is finished
        write(AUDIO_OUTPUT_PATH, AUDIO_SAMPLE_RATE, audio_data)
        transcript = stt(AUDIO_OUTPUT_PATH)
    except Exception as e:
        print(f"\t{node}🖥️❌ exception in STT: {e}")
        return f"{node}👂❌ error with stt", ""
    return f"{node}👂✅ stt heard [{transcript}]", transcript
