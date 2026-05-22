from flask import Flask, request, jsonify, render_template, session
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "random_secret_123"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
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
        messages=session["messages"]
    )

    reply = response.choices[0].message.content
    session["messages"].append({"role": "assistant", "content": reply})
    session.modified = True

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)