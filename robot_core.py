from voice_engine import VoiceEngine
from brain_engine import BrainEngine
from tts_engine import TTSEngine
import difflib


class RobotCore:
    def __init__(self):
        self.voice = VoiceEngine("vosk-model-en-us-0.22")
        self.brain = BrainEngine("knowledge/knowledge.txt")
        self.tts = TTSEngine()

    def wake_detect(self, text):
        words = text.lower().split()
        for word in words:
            similarity = difflib.SequenceMatcher(None, word, "hey").ratio()
            if similarity > 0.6:
                return True
        return False

    def run(self):
        print("Elmo is now online.")
        self.tts.speak("Elmo is now online.")

        try:
            while True:
                print("\nListening...")
                text = self.voice.listen()
                print("Heard:", text)

                lowered = text.lower()

                direct_triggers = [
                    "who are you",
                    "what do you do",
                    "what can you do",
                    "raspberry",
                    "how are you"
                ]

                if not self.wake_detect(text) and not any(p in lowered for p in direct_triggers):
                    continue

                cleaned_text = lowered.replace("hey", "").strip()
                response = self.brain.generate(cleaned_text)

                print("Response:", response)
                self.tts.speak(response)

        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            self.tts.speak("Shutting down.")