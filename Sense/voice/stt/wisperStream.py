#!/usr/bin/env python3
import sys
import numpy as np
import whisper
import whisper_timestamped
import librosa
from functools import lru_cache
import torch
import time
from mosestokenizer import MosesTokenizer
import json


@lru_cache
def load_audio(fname):
    a, _ = librosa.load(fname, sr=16000)
    return a

def load_audio_chunk(fname, beg, end):
    audio = load_audio(fname)
    beg_s = int(beg*16000)
    end_s = int(end*16000)
    return audio[beg_s:end_s]

class WhisperASR:
    def __init__(self, modelsize="small", lan="en", cache_dir="disk-cache-dir"):
        self.original_language = lan 
        self.model = whisper.load_model(modelsize, download_root=cache_dir)

    def transcribe(self, audio, init_prompt=""):
        result = whisper_timestamped.transcribe_timestamped(self.model, audio, language=self.original_language, initial_prompt=init_prompt, verbose=None, condition_on_previous_text=True)
        return result
 
    def ts_words(self,r):
        # return: transcribe result object to [(beg,end,"word1"), ...]
        o = []
        for s in r["segments"]:
            for w in s["words"]:
                t = (w["start"],w["end"],w["text"])
                o.append(t)
        return o

def to_flush(sents, offset=0):
    # concatenates the timestamped words or sentences into one sequence that is flushed in one line
    # sents: [(beg1, end1, "sentence1"), ...] or [] if empty
    # return: (beg1,end-of-last-sentence,"concatenation of sentences") or (None, None, "") if empty
    t = " ".join(s[2] for s in sents)
    if len(sents) == 0:
        b = None
        e = None
    else:
        b = offset + sents[0][0]
        e = offset + sents[-1][1]
    return (b,e,t)

class HypothesisBuffer:

    def __init__(self):
        self.commited_in_buffer = []
        self.buffer = []
        self.new = []

        self.last_commited_time = 0
        self.last_commited_word = None

    def insert(self, new, offset):
        # compare self.commited_in_buffer and new. It inserts only the words in new that extend the commited_in_buffer, it means they are roughly behind last_commited_time and new in content
        # the new tail is added to self.new
        
        new = [(a+offset,b+offset,t) for a,b,t in new]
        self.new = [(a,b,t) for a,b,t in new if a > self.last_commited_time-0.1]

        if len(self.new) >= 1:
            a,b,t = self.new[0]
            if abs(a - self.last_commited_time) < 1:
                if self.commited_in_buffer:
                    # it's going to search for 1, 2 or 3 consecutive words that are identical in commited and new. If they are, they're dropped.
                    cn = len(self.commited_in_buffer)
                    nn = len(self.new)
                    for i in range(1,min(min(cn,nn),5)+1):
                        c = " ".join([self.commited_in_buffer[-j][2] for j in range(1,i+1)][::-1])
                        tail = " ".join(self.new[j-1][2] for j in range(1,i+1))
                        if c == tail:
                            print("removing last",i,"words:",file=sys.stderr)
                            for j in range(i):
                                print("\t",self.new.pop(0),file=sys.stderr)
                            break

    def flush(self):
        # returns commited chunk = the longest common prefix of 2 last inserts. 

        commit = []
        while self.new:
            na, nb, nt = self.new[0]

            if len(self.buffer) == 0:
                break

            if nt == self.buffer[0][2]:
                commit.append((na,nb,nt))
                self.last_commited_word = nt
                self.last_commited_time = nb
                self.buffer.pop(0)
                self.new.pop(0)
            else:
                break
        self.buffer = self.new
        self.new = []
        self.commited_in_buffer.extend(commit)
        return commit

    def pop_commited(self, time):
        while self.commited_in_buffer and self.commited_in_buffer[0][1] <= time:
            self.commited_in_buffer.pop(0)

    def complete(self):
        return self.buffer

class OnlineASRProcessor:

    SAMPLING_RATE = 16000

    def __init__(self, language, asr, chunk):
        """language: lang. code
        asr: WhisperASR object
        chunk: number of seconds for intended size of audio interval that is inserted and looped
        """
        self.language = language
        self.asr = asr
        self.tokenizer = MosesTokenizer("en")

        self.init()

        self.chunk = chunk


    def init(self):
        """run this when starting or restarting processing"""
        self.audio_buffer = np.array([],dtype=np.float32)
        self.buffer_time_offset = 0

        self.transcript_buffer = HypothesisBuffer()
        self.commited = []
        self.last_chunked_at = 0

        self.silence_iters = 0

    def insert_audio_chunk(self, audio):
        self.audio_buffer = np.append(self.audio_buffer, audio)

    def prompt(self):
        """Returns a tuple: (prompt, context), where "prompt" is a 200-character suffix of commited text that is inside of the scrolled away part of audio buffer. 
        "context" is the commited text that is inside the audio buffer. It is transcribed again and skipped. It is returned only for debugging and logging reasons.
        """
        k = max(0,len(self.commited)-1)
        while k > 0 and self.commited[k-1][1] > self.last_chunked_at:
            k -= 1

        p = self.commited[:k]
        p = [t for _,_,t in p]
        prompt = []
        l = 0
        while p and l < 200:  # 200 characters prompt size
            x = p.pop(-1)
            l += len(x)+1
            prompt.append(x)
        non_prompt = self.commited[k:]
        return " ".join(prompt[::-1]), " ".join(t for _,_,t in non_prompt)

    def process_iter(self):
        """Runs on the current audio buffer.
        Returns: a tuple (beg_timestamp, end_timestamp, "text"), or (None, None, ""). 
        The non-emty text is confirmed (commited) partial transcript.
        """

        prompt, non_prompt = self.prompt()
        print("PROMPT:", prompt, file=sys.stderr)
        print("CONTEXT:", non_prompt, file=sys.stderr)
        print(f"transcribing {len(self.audio_buffer)/self.SAMPLING_RATE:2.2f} seconds from {self.buffer_time_offset:2.2f}",file=sys.stderr)
        res = self.asr.transcribe(self.audio_buffer, init_prompt=prompt)

        # transform to [(beg,end,"word1"), ...]
        tsw = self.asr.ts_words(res)

        self.transcript_buffer.insert(tsw, self.buffer_time_offset)
        o = self.transcript_buffer.flush()
        self.commited.extend(o)
        print(">>>>COMPLETE NOW:",to_flush(o),file=sys.stderr,flush=True)
        print("INCOMPLETE:",to_flush(self.transcript_buffer.complete()),file=sys.stderr,flush=True)

        # there is a newly confirmed text
        if o:
            # we trim all the completed sentences from the audio buffer
            self.chunk_completed_sentence()

            # ...segments could be considered
            #self.chunk_completed_segment(res)

            # 
#            self.silence_iters = 0

         # this was an attempt to trim silence/non-linguistic noise detected by the fact that Whisper doesn't transcribe anything for 3-times in a row.
         # It seemed not working better, or needs to be debugged.

#        elif self.transcript_buffer.complete():
#            self.silence_iters = 0
#        elif not self.transcript_buffer.complete():
#        #    print("NOT COMPLETE:",to_flush(self.transcript_buffer.complete()),file=sys.stderr,flush=True)
#            self.silence_iters += 1
#            if self.silence_iters >= 3:
#                n = self.last_chunked_at
##                self.chunk_completed_sentence()
##                if n == self.last_chunked_at:
#                self.chunk_at(self.last_chunked_at+self.chunk)
#                print(f"\tCHUNK: 3-times silence! chunk_at {n}+{self.chunk}",file=sys.stderr)
##                self.silence_iters = 0


        # if the audio buffer is longer than 30s, trim it...
        if len(self.audio_buffer)/self.SAMPLING_RATE > 30:
            # ...on the last completed segment (labeled by Whisper)
            self.chunk_completed_segment(res)

            # alternative: on any word
            #l = self.buffer_time_offset + len(self.audio_buffer)/self.SAMPLING_RATE - 10
            # let's find commited word that is less
            #k = len(self.commited)-1
            #while k>0 and self.commited[k][1] > l:
            #    k -= 1
            #t = self.commited[k][1] 
            print(f"chunking because of len",file=sys.stderr)
            #self.chunk_at(t)

        print(f"len of buffer now: {len(self.audio_buffer)/self.SAMPLING_RATE:2.2f}",file=sys.stderr)
        return to_flush(o)

    def chunk_completed_sentence(self):
        if self.commited == []: return
        print(self.commited,file=sys.stderr)
        sents = self.words_to_sentences(self.commited)
        for s in sents:
            print("\t\tSENT:",s,file=sys.stderr)
        if len(sents) < 2:
            return
        while len(sents) > 2:
            sents.pop(0)
        # we will continue with audio processing at this timestamp
        chunk_at = sents[-2][1]

        print(f"--- sentence chunked at {chunk_at:2.2f}",file=sys.stderr)
        self.chunk_at(chunk_at)

    def chunk_completed_segment(self, res):
        if self.commited == []: return

        ends = [s["end"] for s in res["segments"]]

        t = self.commited[-1][1]

        if len(ends) > 1:

            e = ends[-2]+self.buffer_time_offset
            while len(ends) > 2 and e > t:
                ends.pop(-1)
                e = ends[-2]+self.buffer_time_offset
            if e <= t:
                print(f"--- segment chunked at {e:2.2f}",file=sys.stderr)
                self.chunk_at(e)
            else:
                print(f"--- last segment not within commited area",file=sys.stderr)
        else:
            print(f"--- not enough segments to chunk",file=sys.stderr)





    def chunk_at(self, time):
        """trims the hypothesis and audio buffer at "time"
        """
        self.transcript_buffer.pop_commited(time)
        cut_seconds = time - self.buffer_time_offset
        self.audio_buffer = self.audio_buffer[int(cut_seconds)*self.SAMPLING_RATE:]
        self.buffer_time_offset = time
        self.last_chunked_at = time

    def words_to_sentences(self, words):
        """Uses mosestokenizer for sentence segmentation of words.
        Returns: [(beg,end,"sentence 1"),...]
        """
        
        cwords = [w for w in words]
        t = " ".join(o[2] for o in cwords)
        s = self.tokenizer.split(t)
        out = []
        while s:
            beg = None
            end = None
            sent = s.pop(0).strip()
            fsent = sent
            while cwords:
                b,e,w = cwords.pop(0)
                if beg is None and sent.startswith(w):
                    beg = b
                elif end is None and sent == w:
                    end = e
                    out.append((beg,end,fsent))
                    break
                sent = sent[len(w):].strip()
        return out

    def finish(self):
        """Flush the incomplete text when the whole processing ends.
        Returns: the same format as self.process_iter()
        """
        o = self.transcript_buffer.complete()
        f = to_flush(o)
        print("last, noncommited:",f,file=sys.stderr)
        return f



## main:

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('audio_path', type=str, help="Filename of 16kHz mono channel wav, on which live streaming is simulated.")
parser.add_argument('--min-chunk-size', type=float, default=1.0, help='Minimum audio chunk size in seconds. It waits up to this time to do processing. If the processing takes shorter time, it waits, otherwise it processes the whole segment that was received by this time.')
parser.add_argument('--model', type=str, default='large-v2', help="name of the Whisper model to use (default: large-v2, options: {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}")
parser.add_argument('--model_dir', type=str, default='disk-cache-dir', help="the path where Whisper models are saved (or downloaded to). Default: ./disk-cache-dir")
parser.add_argument('--lan', '--language', type=str, default='en', help="Language code for transcription, e.g. en,de,cs.")
parser.add_argument('--start_at', type=float, default=0.0, help='Start processing audio at this time.')
args = parser.parse_args()

audio_path = args.audio_path

SAMPLING_RATE = 16000
duration = len(load_audio(audio_path))/SAMPLING_RATE
print("Audio duration is: %2.2f seconds" % duration, file=sys.stderr)

size = args.model
language = args.lan

t = time.time()
print(f"Loading Whisper {size} model for {language}...",file=sys.stderr,end=" ",flush=True)
asr = WhisperASR(lan=language, modelsize=size)
e = time.time()
print(f"done. It took {round(e-t,2)} seconds.",file=sys.stderr)


min_chunk = args.min_chunk_size
online = OnlineASRProcessor(language,asr,min_chunk)


# load the audio into the LRU cache before we start the timer
a = load_audio_chunk(audio_path,0,1)

# warm up the ASR, because the very first transcribe takes much more time than the other
asr.transcribe(a)

def output_transcript(o):
    # output format in stdout is like:
    # 4186.3606 0 1720 Takhle to je
    # - the first three words are:
    #    - emission time from beginning of processing, in milliseconds
    #    - beg and end timestamp of the text segment, as estimated by Whisper model. The timestamps are not accurate, but they're useful anyway
    # - the next words: segment transcript
    now = time.time()-start
    if o[0] is not None:
        print("%1.4f %1.0f %1.0f %s" % (now*1000, o[0]*1000,o[1]*1000,o[2]),flush=True)
    else:
        print(o,file=sys.stderr,flush=True)

beg = args.start_at
end = 0
start = time.time()-beg
while True:
    now = time.time() - start
    if now < end+min_chunk:
        time.sleep(min_chunk+end-now)
    end = time.time() - start
    a = load_audio_chunk(audio_path,beg,end)
    beg = end
    online.insert_audio_chunk(a)

    try:
        o = online.process_iter()
    except AssertionError:
        print("assertion error",file=sys.stderr)
        pass
    else:
        output_transcript(o)
    now = time.time() - start
    print(f"## last processed {end:.2f} s, now is {now:.2f}, the latency is {now-end:.2f}",file=sys.stderr)

    print(file=sys.stderr,flush=True)

    if end >= duration:
        break

o = online.finish()
output_transcript(o)