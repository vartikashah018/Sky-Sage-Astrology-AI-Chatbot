from flask import Flask, request, jsonify, render_template
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import random

app = Flask(__name__)

# Zodiac signs list
zodiac_signs = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"
]

# Load Hugging Face models
conversation_pipeline = pipeline("text-generation", model="google/flan-t5-base")

horoscope_tokenizer = AutoTokenizer.from_pretrained("shahp7575/gpt2-horoscopes")
horoscope_model = AutoModelForCausalLM.from_pretrained("shahp7575/gpt2-horoscopes")

# Tarot logic
def get_tarot_reply():
    responses = [
        "🃏 The Sun – Yes",
        "🎴 The Moon – No",
        "🪄 The Fool – Maybe, trust your instincts",
        "🧙 The Magician – Yes, with effort",
        "⛓️ The Devil – No, reconsider your path"
    ]
    return f"🔮 Tarot says: {random.choice(responses)}"

# Horoscope logic (improved)
def generate_horoscope(sign):
    prompt = f"Horoscope for {sign.capitalize()} today:"
    input_ids = horoscope_tokenizer.encode(prompt, return_tensors="pt")
    output = horoscope_model.generate(
        input_ids,
        max_length=70,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )
    result = horoscope_tokenizer.decode(output[0], skip_special_tokens=True)
    cleaned = result.replace(prompt, "").strip().split(".")[0] + "."
    return f"🔮 {sign.capitalize()} Horoscope: {cleaned}"

# General AI conversation
def generate_conversation(message):
    response = conversation_pipeline(message, max_length=60, do_sample=True)[0]['generated_text']
    return response.strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip().lower()

    if user_message in zodiac_signs:
        reply = generate_horoscope(user_message)
    elif any(kw in user_message for kw in ["yes", "no", "should", "will", "can I", "do I"]):
        reply = get_tarot_reply()
    else:
        reply = generate_conversation(user_message)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
