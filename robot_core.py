from voice_engine import VoiceEngine
from brain_engine import BrainEngine
from tts_engine import TTSEngine
import re


class RobotCore:
    def __init__(self):
        self.voice = VoiceEngine("vosk-model-small-en-us-0.15")
        self.brain = BrainEngine("knowledge/knowledge.txt")
        self.tts = TTSEngine()

        # Wake word
        self.wake_word = "hello"

    def clean_transcript(self, text):
        """
        Clean transcript safely.
        Removes standalone 'the' only.
        Does NOT break words like 'weather' or 'whether'.
        """
        text = text.lower()

        # Remove standalone 'the'
        text = re.sub(r"\bthe\b", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def run(self):
        print("Elmo is now online.")
        self.tts.speak("Elmo is now online.")

        try:
            while True:
                print("\nListening...")
                text = self.voice.listen()

                if not text:
                    continue

                print("Heard:", text)

                lowered = text.lower()

                # STRICT wake word detection (as word)
                words = lowered.split()
                if self.wake_word not in words:
                    continue

                # Remove wake word
                command = re.sub(r"\b" + self.wake_word + r"\b", "", lowered).strip()

                # Clean safely
                command = self.clean_transcript(command)

                if not command:
                    self.tts.speak("Yes?")
                    continue

                print("Command:", command)

                response = self.brain.generate(command)

                print("Response:", response)
                self.tts.speak(response)

        except KeyboardInterrupt:
            print("\nShutting down gracefully...")
            self.tts.speak("Shutting down.")