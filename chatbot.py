import nltk
import tkinter as tk
from tkinter import Scrollbar, Text
from PIL import Image, ImageTk
import json
import numpy as np
import random
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

# nltk.download('punkt')
# nltk.download('stopwords')

# Load intents
with open("intents.json", "r") as file:
    intents = json.load(file)

stem = PorterStemmer()
stop_word = set(stopwords.words("english"))

# Preprocessing function
def preprocess(sentence):
    words = nltk.word_tokenize(sentence.lower())
    words = [w for w in words if w not in stop_word]
    words = [stem.stem(w) for w in words]
    return words

# Get matching tag
def get_intent_tag(user_input):
    input_words = preprocess(user_input)
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_words = preprocess(pattern)
            if any(word in pattern_words for word in input_words):
                return intent['tag']
    return None

# Generate response
def get_response(tag):
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return np.random.choice(intent['responses'])
    return "I'm sorry, I didn't understand that."

# Chat class with Tkinter GUI
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x600")
        self.root.title("ChatGuru - Your Friendly Chatbot")

        # Chat area
        self.chat_area = Text(root, bd=1, bg="white", width=50, height=20, wrap="word", font=("Arial", 12))
        self.chat_area.pack(pady=10)

        # Scrollbar
        scrollbar = Scrollbar(root, command=self.chat_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_area['yscrollcommand'] = scrollbar.set

        # Entry box
        self.entry_box = tk.Entry(root, bd=1, width=40, font=("Arial", 12))
        self.entry_box.pack(padx=10, pady=5, side=tk.LEFT)

        # Send button
        self.send_btn = tk.Button(root, text="Send", command=self.send_message, font=("Arial", 12), bg="#0084ff", fg="white")
        self.send_btn.pack(padx=5, pady=5, side=tk.LEFT)

    def send_message(self):
        user_input = self.entry_box.get()
        self.chat_area.insert(tk.END, f"You: {user_input}\n")
        self.entry_box.delete(0, tk.END)

        if user_input.lower() == "quit":
            self.chat_area.insert(tk.END, "ChatGuru: Goodbye! 👋\n")
            return

        tag = get_intent_tag(user_input)
        if tag:
            response = get_response(tag)
        else:
            response = "I'm not sure I understand. Can you try something else?"

        self.chat_area.insert(tk.END, f"ChatGuru: {response}\n")

# Run GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
