import pyttsx3


class TTSEngine:
    def __init__(self):
        # Do not initialize engine here
        # We will create a fresh engine every time we speak
        pass

    def speak(self, text):
        try:
            # Create a new engine instance every time (prevents freeze)
            engine = pyttsx3.init()

            engine.setProperty("rate", 160)
            engine.setProperty("volume", 1.0)

            engine.say(text)
            engine.runAndWait()
            engine.stop()

            # Explicit cleanup
            del engine

        except Exception as e:
            print("TTS Error:", e)