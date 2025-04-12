import requests
import os
from dotenv import load_dotenv
from rich import print
from rich.console import Console
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    'x-apisports-key': API_KEY
}

# Bugünün tarihi
today = datetime.now().strftime('%Y-%m-%d')

# Türkiye Süper Lig maçlarını çek (id=203)
url = f"https://v3.football.api-sports.io/fixtures?date={today}&league=203&season=2023"

response = requests.get(url, headers=headers)
data = response.json()

console = Console()
console.rule("[bold green]Canlı Maç Listesi")

for match in data["response"]:
    teams = match["teams"]
    goals = match["goals"]
    status = match["fixture"]["status"]["long"]
    time = match["fixture"]["date"][11:16]  # saat:dk
    home = teams["home"]["name"]
    away = teams["away"]["name"]
    score = f'{goals["home"]}-{goals["away"]}' if goals["home"] is not None else "0-0"

    print(f"[cyan]{time}[/cyan] | [bold]{home}[/bold] vs [bold]{away}[/bold] | [yellow]{score}[/yellow] | [green]{status}[/green]")
