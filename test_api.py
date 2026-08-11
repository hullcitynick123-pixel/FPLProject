import requests

API_KEY = ""

url = "https://v3.football.api-sports.io/leagues"
headers = {
    'x-apisports-key': API_KEY
}

try:
    payload={}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

except Exception as e:
    print(f"\n❌ Connection Failed: {e}")