#!/usr/bin/env python3

import speech_recognition as sr
from os import path, listdir

dat = listdir("out/")
dat2 = [ int(d[2:-4]) for d in dat if d[0] == '2']
dat2.sort()

for files in dat2:
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "out/2." + str(files) + ".wav")
    print(AUDIO_FILE)
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        print(r.recognize_google(audio))
    except sr.UnknownValueError:
        print("")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
