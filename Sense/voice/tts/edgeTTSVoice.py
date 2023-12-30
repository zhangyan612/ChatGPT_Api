#!/usr/bin/env python3

"""
Fastest TTS engine
"""
import asyncio
import time
import os
import vlc
import edge_tts

def playSound(file):
    p = vlc.MediaPlayer(file)
    p.play()
    time.sleep(1)
    while p.is_playing():
        time.sleep(1)

async def generate_voice(text="Hello this is a test run", voice="en-US-SteffanNeural"):
    # Generate a timestamp for the output file name
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # Get the current working directory
    cwd = os.getcwd()
    output_file = os.path.join(cwd, f"Sense/voice/tts/generated/{timestamp}.mp3")

    communicate = edge_tts.Communicate(text, voice)
    with open(output_file, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

    # Play the generated audio file
    playSound(output_file)

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(generate_voice())
    finally:
        loop.close()



# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, ChristopherNeural)', 'ShortName': 'en-US-ChristopherNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Christopher Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Reliable', 'Authority']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, EricNeural)', 'ShortName': 'en-US-EricNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Eric Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Rational']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)', 'ShortName': 'en-US-GuyNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Guy Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Passion']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, RogerNeural)', 'ShortName': 'en-US-RogerNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Roger Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Lively']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, SteffanNeural)', 'ShortName': 'en-US-SteffanNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Steffan Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Rational']}, 'Language': 'en'}]
