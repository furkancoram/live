from flask import Flask, render_template_string
import requests, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/")
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}&league=203&season=2023"
    headers = {'x-apisports-key': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    output = ""
    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        goals = match["goals"]
        score = f'{goals["home"]}-{goals["away"]}' if goals["home"] is not None else "0-0"
        output += f"<li>{home} vs {away} — {score}</li>"

    return render_template_string(f"""
        <h1>Canlı Maçlar</h1>
        <ul>{output}</ul>
    """)

if __name__ == "__main__":
    app.run(debug=True)
