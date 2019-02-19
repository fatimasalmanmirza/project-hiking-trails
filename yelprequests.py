import requests
import os
import random

key = os.environ["YELP_API_KEY"]

headers = {"Authorization": 'Bearer ' + key}
payload = {"term": "hiking trails", "location": "los angeles"}
r = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=payload)
hiking_trails = r.json()

list_of_trails_tuples = []
list_trails_info = hiking_trails["businesses"]
for trails in list_trails_info:
    
    names = trails["name"]
    ratings = trails["rating"]
    address = trails["location"]
    if ratings >= 4:
        list_of_trails_tuples.append((names, ratings, address))
# print(random.choice(list_of_trails_tuples))  
print(random.choice(list_of_trails_tuples)) 





# print(hiking_trails)