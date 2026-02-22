import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

BASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

def load_file(filename):
    with open(os.path.join(BASE_PATH, filename), "r", encoding="utf-8") as f:
        return f.read()

def get_response(user_text, knowledge_unused=None):

    if not user_text:
        return "I couldn't hear you clearly."

    text = user_text.lower()

    # Greetings
    if any(word in text for word in ["hi", "hello", "hey"]):
        return "Hello! I am your department assistant. How can I help you?"

    if any(word in text for word in ["bye", "goodbye", "stop"]):
        return "Goodbye! Have a nice day."

    # Intent-based file selection
    if any(word in text for word in ["hod", "head", "advisor", "faculty", "professor"]):
        context = load_file("faculty_profiles.txt")

    elif any(word in text for word in ["lab", "laboratory"]):
        context = load_file("labs.txt")

    

    elif any(word in text for word in ["program", "course", "btech", "mtech"]):
        context = load_file("programs.txt")

    elif any(word in text for word in ["mission", "vision", "college"]):
        context = load_file("department_data.txt")

    else:
        context = load_file("department_data.txt")

    prompt = f"""
You are a highly accurate department assistant AI.

Answer strictly using ONLY the provided information.
If the answer is not present, say:
"I do not have that information."

Information:
{context}

Question:
{user_text}

Answer:
"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_length=200)

    return tokenizer.decode(outputs[0], skip_special_tokens=True)
