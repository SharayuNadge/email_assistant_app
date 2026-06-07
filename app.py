from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_input = data["user_input"]
    tone = data["tone"]
    user_name = data.get("user_name", "")
    user_role = data.get("user_role", "")
    recipient_name = data.get("recipient_name", "")

    messages = [
        {"role": "system", "content": """You are a professional email writing assistant.
            Always respond with a JSON object only - no extra text, no markdown, no code blocks.
            The JSON must have exactly these three fields:
            - subject: the email subject line
            - body: the full email body. Use \\n for new lines between paragraphs and after greetings and sign offs.
            - tone: the tone specified by the user - formal, casual or persuasive
            Always follow the tone specified by the user strictly.
            If the email requires specific details the user hasn't provided (date, time, location, project name etc.), include clear placeholders like [Date], [Time], [Location].
            IMPORTANT: Always write the email in professional English ONLY, regardless of what language the user types in. Never respond in any other language.
         """},
        {"role": "user", "content": f"{user_input}. Use a {tone} tone. Address the recipient as '{recipient_name if recipient_name else '[Recipient Name]'}' in the salutation. Sign off with the sender's name '{'[Your Name]' if not user_name else user_name}' and their role '{'[Your Role]' if not user_role else user_role}'."}
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000
        )

        raw = response.choices[0].message.content
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
        email_data = json.loads(raw)
        email_data["body"] = email_data["body"].replace("\\n", "\n")
        return jsonify(email_data)

    except Exception as e:
        if "connection" in str(e).lower():
            return jsonify({"error": "Cannot connect to Groq. Check your API key and internet connection!"}), 500
        raise e
    except json.JSONDecodeError:
        return jsonify({"error": "AI returned invalid response. Please try again."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)