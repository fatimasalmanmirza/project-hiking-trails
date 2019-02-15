import requests
import os

key = os.environ["YELP_API_KEY"]

headers = {"Authorization": 'Bearer ' + key}
payload = {"term": "hiking trails", "location": "fremont"}
r = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=payload)
hiking_trails = r.json()
print(hiking_trails)