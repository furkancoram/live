from flask import Flask, render_template_string
import requests, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

@app.route("/")
def index():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {'x-apisports-key': API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()

    if not data["response"]:
        return "<h2>Bugün hiçbir ligde maç yok gibi 😢</h2>"

    html_content = """
    <html>
    <head>
        <title>Canlı Maçlar</title>
        <style>
            body { font-family: Arial; background-color: #f4f4f4; color: #222; padding: 20px; }
            h1 { color: #0077cc; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; background: white; padding: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
            .skor { font-weight: bold; color: #e60000; }
            .status { color: gray; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>Canlı Maçlar</h1>
        <ul>
    """

    for match in data["response"]:
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]
        goals = match["goals"]
        status = match["fixture"]["status"]["long"]
        time = match["fixture"]["date"][11:16]
        score = f'{goals["home"]}-{goals["away"]}' if goals["home"] is not None else "0-0"

        html_content += f"""
        <li>
            <span>{time} | {home} vs {away} — <span class='skor'>{score}</span></span><br>
            <span class='status'>{status}</span>
        </li>
        """

    html_content += "</ul></body></html>"
    return html_content

if __name__ == "__main__":
    app.run(debug=True)
