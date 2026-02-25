import pyttsx3

engine = pyttsx3.init(driverName='sapi5')
engine.setProperty('rate', 160)

voices = engine.getProperty('voices')
print(voices)

engine.say("Hello. Voice test working.")
engine.runAndWait()