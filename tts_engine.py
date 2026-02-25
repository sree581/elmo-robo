import pyttsx3


class TTSEngine:
    def __init__(self):
        pass

    def speak(self, text):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 165)
            engine.setProperty("volume", 1.0)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine
        except Exception as e:
            print("TTS Error:", e)