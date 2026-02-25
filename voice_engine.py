import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer


class VoiceEngine:
    def __init__(self, model_path):
        self.q = queue.Queue()
        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def listen(self):
        self.rec.Reset()

        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=self.callback
        ):
            while True:
                data = self.q.get()

                if self.rec.AcceptWaveform(data):
                    result = json.loads(self.rec.Result())
                    text = result.get("text", "").strip()

                    # Filter garbage noise
                    if not text:
                        continue

                    if text in ["the", "a", "an"]:
                        continue

                    # Ignore single short words
                    if len(text.split()) == 1 and len(text) <= 3:
                        continue

                    return text