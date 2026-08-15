import http.client

import config

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-apisports-key': config.API_KEY
    }

conn.request("GET", "/players?id=276&season=2019", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

