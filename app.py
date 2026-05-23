from flask import Flask, request, jsonify, render_template, session
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "codegenie_secret_123"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert coding assistant. Help developers with writing code, debugging, explaining concepts, and code reviews. Always format code in proper markdown code blocks with the language specified."""

@app.route("/")
def home():
    if "messages" not in session:
        session["messages"] = []
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if "messages" not in session:
        session["messages"] = []
    session["messages"].append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + session["messages"]
    )
    reply = response.choices[0].message.content
    session["messages"].append({"role": "assistant", "content": reply})
    session.modified = True
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear():
    session["messages"] = []
    return jsonify({"status": "cleared"})

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify(session.get("messages", []))

if __name__ == "__main__":
    app.run(debug=True)