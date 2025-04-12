from flask import Flask, render_template
import requests, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/")
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    headers = { 'x-apisports-key': API_KEY }

    url = f"https://v3.football.api-sports.io/fixtures?date={today}&league=203"
    response = requests.get(url, headers=headers)
    data = response.json()

    # API'den gelen veri sayısını Render loglarında görmek için:
    print("API'den gelen maç sayısı:", len(data["response"]))

    matches = []
    if not data["response"]:
        return render_template("index.html", matches=[], message="Bugün Süper Lig'de maç yok gibi görünüyor.")

    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        score_home = match["goals"]["home"]
        score_away = match["goals"]["away"]
        time = match["fixture"]["status"]["elapsed"]
        status = match["fixture"]["status"]["long"]
        logo_home = match["teams"]["home"]["logo"]
        logo_away = match["teams"]["away"]["logo"]

        matches.append({
            "home": home,
            "away": away,
            "score": f"{score_home} - {score_away}" if score_home is not None else "0 - 0",
            "time": time if time else "⏳",
            "status": status,
            "logo_home": logo_home,
            "logo_away": logo_away
        })

    return render_template("index.html", matches=matches)
