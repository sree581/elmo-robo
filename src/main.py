from speech_to_text import listen
from brain import get_response
from text_to_speech import speak

print("🚀 Humanoid Robot Activated")

with open("data/department_data.txt", "r") as f:
    knowledge = f.readlines()

while True:
    user_text = listen()

    if not user_text:
        continue

    if "stop" in user_text.lower() or "bye" in user_text.lower():
        speak("Goodbye.")
        break

    response = get_response(user_text)
    speak(response)
