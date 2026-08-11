import requests

API_KEY = ""
HEADERS = {'x-apisports-key': API_KEY}

# Test 1: Try general player stats endpoint for League 39
url = "https://v3.football.api-sports.io/players"
params = {'league': 39, 'season': 2026, 'page': 1}

response = requests.get(url, headers=HEADERS, params=params)

print(f"Status Code: {response.status_code}")
print("Response Text:", response.text)