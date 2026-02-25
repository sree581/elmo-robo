class BrainEngine:
    def __init__(self, knowledge_path):
        self.knowledge = self.load_knowledge(knowledge_path)

    def load_knowledge(self, path):
        lines = []
        try:
            with open(path, "r") as f:
                for line in f:
                    clean = line.strip()
                    if clean:
                        lines.append(clean)
        except FileNotFoundError:
            print("Knowledge file not found.")
        return lines

    def generate(self, text):
        text = text.lower().strip()

        # Built-in intents
        if "who are you" in text:
            return "I am Elmo, your offline robotic assistant."

        if "how are you" in text:
            return "I am functioning properly and ready to assist you."

        if "what do you do" in text or "what can you do" in text:
            return "I can answer questions from my knowledge base and assist with robotic commands."

        if "are you offline" in text:
            return "Yes. I run fully offline."

        if "raspberry pi" in text:
            return "Raspberry Pi is a small single board computer used for robotics and embedded systems."

        if "shutdown" in text or "stop" in text:
            return "Shutting down system."

        # Knowledge-based matching
        best_match = None
        best_score = 0

        for line in self.knowledge:
            score = 0
            for word in text.split():
                if word in line.lower():
                    score += 1

            if score > best_score:
                best_score = score
                best_match = line

        if best_match and best_score > 0:
            return best_match

        return "I do not have that information."