from flask import Flask, render_template, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key="paste your OpenAI API key here")  

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please type a message."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that ONLY answers questions related to Brawl Stars. "
                        "Respond politely to greetings and explain your capabilities. "
                        "Format answers using Markdown with clear headings, bullet points, bold text, and line breaks. "
                        "If asked about something unrelated, politely redirect the user to game-related topics."
                    )
                },
                {"role": "user", "content": user_message}
            ]
        )

        ai_reply = response.choices[0].message.content
        return jsonify({"response": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
