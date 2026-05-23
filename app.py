from flask import Flask, request, jsonify, render_template, session
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()


app = Flask(__name__)
app.secret_key = "codegenie_secret_123"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HISTORY_FILE = "chat_history.json"

SYSTEM_PROMPT = """You are an expert coding assistant. You help developers with:
- Writing clean, efficient code
- Debugging errors
- Explaining programming concepts
- Code reviews and improvements
- System design and architecture

Always format code in proper markdown code blocks with the language specified.
Be concise but thorough. If you show code, explain what it does."""

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(load_history())

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    messages = load_history()
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    save_history(messages)
    
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    save_history([])
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)