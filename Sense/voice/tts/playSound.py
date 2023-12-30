
import os
import time
import vlc

OUTPUT_FILE = f"20231229-152351.mp3"

cwd = os.getcwd()
print(cwd)
OUTPUT_FILE = os.path.join(cwd, f"Sense/voice/tts/generated/{OUTPUT_FILE}")
print(OUTPUT_FILE)

# both solution works but need to add sleep for the duration of video

def playSound(file):
    p = vlc.MediaPlayer(file)
    p.play()

    time.sleep(1)
    while p.is_playing():
        time.sleep(1)
    # print("The audio has finished playing.")


# from pygame import mixer
# mixer.init()
# mixer.music.load(OUTPUT_FILE)
# mixer.music.play()

# time.sleep(20)



playSound(OUTPUT_FILE)