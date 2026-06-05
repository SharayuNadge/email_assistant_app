from flask import Flask, render_template, request, jsonify
from openai import OpenAI, APIConnectionError
import json

app = Flask(__name__)

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_input = data["user_input"]
    tone = data["tone"]

    messages = [
        {"role": "system", "content": """You are a professional email writing assistant.
Always respond with a JSON object only - no extra text, no markdown, no code blocks.
The JSON must have exactly these three fields:
- subject: the email subject line
- body: the full email body
- tone: the tone specified by the user - formal, casual or persuasive
Always follow the tone specified by the user strictly."""},
        {"role": "user", "content": f"{user_input}. Use a {tone} tone."}
    ]

    try:
        response = client.chat.completions.create(
            model="google/gemma-4-e4b",
            messages=messages,
            max_tokens=1000
        )

        raw = response.choices[0].message.content
        raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
        email_data = json.loads(raw)

        return jsonify(email_data)

    except APIConnectionError:
        return jsonify({"error": "Cannot connect to LM Studio. Make sure server is running!"}), 500

    except json.JSONDecodeError:
        return jsonify({"error": "AI returned invalid response. Please try again."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)