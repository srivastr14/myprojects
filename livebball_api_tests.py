import requests
import json
from datetime import datetime, time
import pytz

tz = pytz.timezone('US/Eastern')
today = datetime.today().strftime('%Y-%m-%d')
midnight = tz.localize(datetime.combine(datetime.now(tz).date(), time(0, 0)), is_dst=None).timestamp()
# print(today, midnight)

url = "https://api.sofascore.com/api/v1/sport/baseball/scheduled-events/" + today

payload = ""
headers = {
    'authority': "api.sofascore.com",
    'cache-control': "max-age=0",
    'sec-ch-ua-mobile': "?0",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    'accept': "*/*",
    'origin': "https://www.sofascore.com",
    'sec-fetch-site': "same-site",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'referer': "https://www.sofascore.com/",
    'accept-language': "en-US,en;q=0.9",
    }

response = requests.request("GET", url, data=payload, headers=headers)

jsondata = json.loads(response.text)

for game in jsondata['events']:
    if game['startTimestamp'] < midnight:
        continue
    if game['tournament']['name'] != "MLB, Regular Season":
        continue
    league = game['tournament']['name']
    hometeam = game['homeTeam']['name']
    awayteam = game['awayTeam']['name']
    if game['status']['description'] == 'Not started':
        print(league, '|', hometeam, "vs", awayteam, "has not started")
        continue
    status = game['status']['description']
    homescore = game['homeScore']['current']
    awayscore = game['awayScore']['current']
    print(league, '|', hometeam, homescore, '-', awayscore, awayteam, status)
