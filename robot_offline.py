import queue
import sounddevice as sd
import json
import os
from vosk import Model, KaldiRecognizer

# Load offline speech model
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

q = queue.Queue()

# ✅ CALLBACK MUST BE DEFINED BEFORE USE
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def speak(text):
    print("🤖 Robot:", text)
    os.system(f'powershell -Command "Add-Type -AssemblyName System.Speech; '
              f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"')

def load_knowledge():
    sections = {}
    current_key = None

    with open("data/department_data.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("[") and line.endswith("]"):
                current_key = line[1:-1].lower()
                sections[current_key] = ""
            elif current_key and line:
                sections[current_key] += line + " "

    return sections

knowledge = load_knowledge()


def get_response(text):
    text = text.lower()

    if "stop" in text or "bye" in text:
        return "Goodbye."

    if "hello" in text or "hi" in text:
        return "Hello. I am your department assistant."

    if "hod" in text or "head" in text:
        return knowledge.get("hod")

    if "vision" in text:
        return knowledge.get("vision")

    if "mission" in text:
        return knowledge.get("mission")

    if "lab" in text:
        return knowledge.get("labs")

    if "program" in text or "course" in text:
        return knowledge.get("programs")

    if "faculty" in text:
        return knowledge.get("faculty")

    if "department" in text:
        return knowledge.get("intro")

    return "Please ask a clear question about the department."
print("🚀 Humanoid Robot Activated (Offline Mode)")
print("🎤 Listening... Speak now!")

with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=callback):

    while True:
        data = q.get()

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            user_text = result.get("text", "").strip()

            if len(user_text) < 3:
                continue

            if user_text:
                print("🗣 You said:", user_text)
                response = get_response(user_text)
                speak(response)

                if "goodbye" in response.lower():
                    break