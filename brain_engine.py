import re

class BrainEngine:
    def __init__(self, knowledge_file):
        self.knowledge = []
        self.stopwords = {
            "the", "is", "a", "an", "who", "what", "when",
            "where", "of", "in", "on", "at", "to", "for",
            "and", "do", "does", "are", "was"
        }

        with open(knowledge_file, "r") as f:
            for line in f:
                if "|" in line:
                    question, answer = line.strip().split("|", 1)
                    self.knowledge.append((question.lower(), answer))

    def clean_text(self, text):
        text = re.sub(r"[^\w\s]", "", text.lower())
        words = text.split()
        words = [w for w in words if w not in self.stopwords]
        return words

    def score(self, query_words, question):
        question_words = self.clean_text(question)
        matches = 0

        for word in query_words:
            if word in question_words:
                matches += 1

        return matches

    def generate(self, text):
        query_words = self.clean_text(text)

        if not query_words:
            return "I didn't understand that."

        best_score = 0
        best_answer = None

        for question, answer in self.knowledge:
            s = self.score(query_words, question)

            if s > best_score:
                best_score = s
                best_answer = answer

        if best_score == 0:
            return "I do not have that information."

        return best_answer