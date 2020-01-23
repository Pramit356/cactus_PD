import os
import speech_recognition as sr

r = sr.Recognizer()
#audio = sr.AudioFile('test.wmv')
audio = r.record('test.wmv', duration=100)
print(r.recognize_google(audio))