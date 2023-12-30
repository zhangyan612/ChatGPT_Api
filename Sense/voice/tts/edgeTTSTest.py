#!/usr/bin/env python3

"""
Fastest TTS engine
"""
import asyncio
import random
import time
import os
import subprocess

import edge_tts
from edge_tts import VoicesManager

TEXT = "Bye Bye"
VOICE = "en-US-SteffanNeural"

# Generate a timestamp for the output file name
timestamp = time.strftime("%Y%m%d-%H%M%S")

# Get the current working directory
cwd = os.getcwd()
print(cwd)
OUTPUT_FILE = os.path.join(cwd, f"Sense/voice/tts/generated/{timestamp}.mp3")
print(OUTPUT_FILE)

# OUTPUT_FILE = f"./generated/{timestamp}.mp3"


async def amain() -> None:
    """Main function"""
    # voices = await VoicesManager.create()
    # voice = voices.find(Gender="Male", Language="en")
    # print(voice)

    communicate = edge_tts.Communicate(TEXT, VOICE)
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                print(f"WordBoundary: {chunk}")

    # Play the generated audio file
    subprocess.call(["mpg123", OUTPUT_FILE])

if __name__ == "__main__":
    loop = asyncio.get_event_loop_policy().get_event_loop()
    try:
        loop.run_until_complete(amain())
    finally:
        loop.close()




# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, ChristopherNeural)', 'ShortName': 'en-US-ChristopherNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Christopher Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Reliable', 'Authority']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, EricNeural)', 'ShortName': 'en-US-EricNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Eric Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Rational']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, GuyNeural)', 'ShortName': 'en-US-GuyNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Guy Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Passion']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, RogerNeural)', 'ShortName': 'en-US-RogerNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Roger Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Lively']}, 'Language': 'en'}, 
# {'Name': 'Microsoft Server Speech Text to Speech Voice (en-US, SteffanNeural)', 'ShortName': 'en-US-SteffanNeural', 'Gender': 'Male', 'Locale': 'en-US', 'SuggestedCodec': 'audio-24khz-48kbitrate-mono-mp3', 'FriendlyName': 'Microsoft Steffan Online (Natural) - English (United States)', 'Status': 'GA', 'VoiceTag': {'ContentCategories': ['News', 'Novel'], 'VoicePersonalities': ['Rational']}, 'Language': 'en'}]
