from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from groq import Groq

# Load env vars
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Create Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question")
    print("QUESTION:", question)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": question}
            ]
        )

        answer = response.choices[0].message.content
        print("ANSWER:", answer)

        return jsonify({"answer": answer})

    except Exception as e:
        print("GROQ ERROR:", e)
        return jsonify({
            "answer": "⚠️ AI service unavailable. Please try again."
        })

if __name__ == "__main__":
    app.run(debug=True)
