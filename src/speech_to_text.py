import speech_recognition as sr

def listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")

        r.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        text = r.recognize_google(audio)
        print("🗣 You said:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        print("Speech service unavailable.")
        return ""
