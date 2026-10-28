from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Read the API key from an environment variable.
# Never write your secret API key directly in this file.
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        message = data.get("message", "").strip()
        mode = data.get("mode", "chat")

        if not message:
            return jsonify({"reply": "Please enter a question."}), 400

        if mode == "quiz":
            prompt = (
                "You are a student assistance chatbot. "
                "Create a quiz based on the student's request. "
                "Include 5 questions and an answer key at the end.\n\n"
                f"Student's request: {message}"
            )
        else:
            prompt = (
                "You are a friendly student assistance chatbot. "
                "Explain concepts in simple, beginner-friendly language. "
                "Use examples when helpful.\n\n"
                f"Student's question: {message}"
            )

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        reply = response.output_text

        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "reply": "Sorry, something went wrong. Check the server configuration and try again."
        }), 500


if __name__ == "__main__":
    app.run(debug=False)
