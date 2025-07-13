from flask import Flask, request, jsonify, render_template
import json
import requests

app = Flask(__name__)

API_TOKEN = "my key"  
API_URL = "https://api.brawlstars.com/v1/brawlers"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

with open("brawlers.json") as f:
    BRAWLERS = json.load(f)

with open("maps.json") as f:
    MAPS = json.load(f)

with open("counters.json") as f:
    COUNTERS = json.load(f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.get_json().get("message", "").lower()
    print(f"User said: {user_input}")
    reply = ""

    for map_name, map_info in MAPS.items():
        if map_name.lower() in user_input:
            enemy_brawlers = [b for b in COUNTERS.keys() if b.lower() in user_input]
            if enemy_brawlers:
                suggestions = []
                for b in enemy_brawlers:
                    suggestions += COUNTERS[b]["counters"]
                recommended = ", ".join(set(suggestions))
                reply = (
                    f"On **{map_name}**, against **{', '.join(enemy_brawlers)}**, consider using: {recommended}.\n"
                    f"These picks help you control the map and win key engagements!"
                )
                print(f"Bot replied: {reply}")
                return jsonify({"response": reply})

    for enemy, data in COUNTERS.items():
        if (
            enemy.lower() in user_input
            and "best" in user_input
            and "counter" in user_input
        ):
            counters = ", ".join(data["counters"])
            reply = (
                f"To counter **{enemy.title()}**, the best picks are: {counters}.\n"
                f"🧠 Strategy: {data['strategy']}"
            )
            print(f"Bot replied: {reply}")
            return jsonify({"response": reply})

    if "counters" in user_input and not any(
        name.lower() in user_input for name in COUNTERS.keys()
    ):
        reply = (
            "You can ask for counters like:\n"
            "- 'Who counters Belle?'\n"
            "- 'To counter Chuck, which brawlers are best?'\n"
            "I'll suggest picks and explain how to beat them!"
        )
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if "best brawler" in user_input or "strongest brawler" in user_input:
        reply = (
            "The best brawler depends on mode and map! Here's a quick guide:\n"
            "- 🏆 Heist: Spike, Barley\n"
            "- 🎯 Bounty: Piper, Belle\n"
            "- ⚽ Brawl Ball: Max, Fang\n"
            "Let me know the mode or map and I’ll give tailored picks!"
        )
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if any(greet in user_input for greet in ["hi", "hello", "hey", "yo"]):
        reply = "Hey! I’m your Brawl Stars assistant. Ask me about brawlers, maps, counters, or strategy!"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if any(
        kw in user_input
        for kw in [
            "how many brawlers",
            "total brawlers",
            "how many characters",
            "total characters",
            "how many heroes",
        ]
    ):
        try:
            response = requests.get(API_URL, headers=HEADERS)
            if response.status_code == 200:
                count = len(response.json().get("items", []))
                reply = f"There are currently **{count} brawlers** in Brawl Stars!"
            else:
                reply = f"API error: {response.json().get('message', 'Unknown error')}"
        except Exception as e:
            reply = f"Could not connect to Brawl Stars API. Details: {e}"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if "how many maps" in user_input or "total maps" in user_input:
        reply = "There are currently **over 700 maps** in Brawl Stars, including official, seasonal, and community maps!"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if any(
        phrase in user_input
        for phrase in [
            "list all maps",
            "show maps",
            "map list",
            "tell me about all the maps",
            "name all maps",
        ]
    ):
        all_maps = ", ".join(MAPS.keys())
        reply = f"Here are the maps I currently know:\n🗺️ {all_maps}"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    if any(
        phrase in user_input
        for phrase in [
            "list all brawlers",
            "name all brawlers",
            "name all brawler",
            "show brawlers",
            "list brawlers",
        ]
    ):
        all_brawlers = ", ".join(BRAWLERS.keys())
        reply = f"Here are the brawlers I know:\n🧍 {all_brawlers}"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    for name, data in BRAWLERS.items():
        if name.lower() in user_input and not any(
            word in user_input for word in ["counter", "beat", "vs", "against"]
        ):
            try:
                response = requests.get(API_URL, headers=HEADERS)
                if response.status_code == 200:
                    brawlers_api = [
                        b["name"].lower() for b in response.json().get("items", [])
                    ]
                    if name.lower() in brawlers_api:
                        powers = ", ".join(data["starPowers"])
                        gadgets = ", ".join(data["gadgets"])
                        reply = (
                            f"**{name}** — {data['bio']}\n"
                            f"🧬 Role: {data['role']}\n"
                            f"⭐ Star Powers: {powers}\n"
                            f"🎯 Gadgets: {gadgets}\n"
                            f"📍 Best Maps: {', '.join(data['bestMaps'])}"
                        )
                    else:
                        reply = (
                            f"{name} is not currently listed in the Brawl Stars API."
                        )
                else:
                    reply = (
                        f"API error: {response.json().get('message', 'Unknown error')}"
                    )
            except Exception as e:
                reply = f"Could not connect to Brawl Stars API. Details: {e}"
            print(f"Bot replied: {reply}")
            return jsonify({"response": reply})

    if "strategy" in user_input:
        reply = "General tip: Use throwers on closed maps, snipers on open maps. Control mid, conserve supers, and pick brawlers that synergize well!"
        print(f"Bot replied: {reply}")
        return jsonify({"response": reply})

    for map_name, info in MAPS.items():
        if map_name.lower() in user_input:
            brawlers = ", ".join(info["recommendedBrawlers"])
            reply = (
                f"**Map**: {map_name} ({info['mode']})\n"
                f"📌 Description: {info['description']}\n"
                f"🔸 Recommended Brawlers: {brawlers}\n"
                f"📊 Strategy: {info['strategy']}"
            )
            print(f"Bot replied: {reply}")
            return jsonify({"response": reply})

    for enemy, data in COUNTERS.items():
        if enemy.lower() in user_input:
            counters = ", ".join(data["counters"])
            reply = (
                f"To counter **{enemy.title()}**, try using: {counters}.\n"
                f"🧠 Strategy: {data['strategy']}"
            )
            print(f"Bot replied: {reply}")
            return jsonify({"response": reply})

    reply = (
        "I didn’t catch that. Try asking:\n"
        "- 'Tell me about Spike'\n"
        "- 'Map is Kaboom Canyon, opponent has Chuck and Frank'\n"
        "- 'How many brawlers are there?'\n"
        "- 'List all maps'\n"
        "- 'Who counters Belle?'"
    )
    print(f"Bot replied: {reply}")
    return jsonify({"response": reply})


if __name__ == "__main__":
    app.run(debug=True)
