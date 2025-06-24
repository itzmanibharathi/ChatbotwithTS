from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)
BOT_NAME = "TS"

GROQ_API_KEY = "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" 

def chatgpt_response(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-70b-8192", 
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def tamil_chatbot(message):
    msg = message.lower().strip()

    if "hi" in msg or "hello" in msg:
        return "Hi da! Enna pandra?"
    if any(x in msg for x in ["how are you", "how r u", "how r you", "how u", "how are u"]):
        return "I'm fine da, how are you? 😊"
    if "i am fine" in msg or "i'm fine" in msg:
        return "Super da! Enna panra ippo? 😁"
    if "bye" in msg:
        return "Bye da! Take care 😇"
    if len(msg) < 3:
        return "Sariya puriyala da, konjam clear-a sollu 😅"

    ai_reply = chatgpt_response(message)
    return ai_reply +" "if ai_reply else "Theriyala da, Google-la thedu pa 😅"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = tamil_chatbot(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
