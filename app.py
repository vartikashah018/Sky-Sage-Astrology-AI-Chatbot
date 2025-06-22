from flask import Flask, request, jsonify, render_template
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline
import torch

app = Flask(__name__)

# Load Horoscope Model (GPT-2)
horoscope_tokenizer = AutoTokenizer.from_pretrained("shahp7575/gpt2-horoscopes")
horoscope_model = AutoModelWithLMHead.from_pretrained("shahp7575/gpt2-horoscopes")

# Load Chatbot Model (DialoGPT)
cchatbot = pipeline("conversational", model="facebook/blenderbot-3B")


# Valid Zodiac signs
VALID_SIGNS = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip().lower()

    # Horoscope Mode
    if user_input in VALID_SIGNS:
        try:
            prompt = f"{user_input.capitalize()} horoscope: "
            inputs = horoscope_tokenizer.encode(prompt, return_tensors="pt")
            outputs = horoscope_model.generate(inputs, max_length=100, do_sample=True)
            horoscope = horoscope_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return jsonify({"reply": horoscope})
        except Exception as e:
            return jsonify({"reply": f"⚠️ Horoscope error: {str(e)}"})

    # Chatbot Mode
    try:
        response = chatbot(f"User: {user_input}\nAI:", max_length=100, num_return_sequences=1)
        reply = response[0]['generated_text'].split("AI:")[-1].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Chatbot error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404 