import json
import os
import requests

with open("json/seat_info.json", "r") as jsonfile:
    seat_info: list[dict[str, str]] = json.load(jsonfile)

if not os.path.exists("json/seat"):
    os.makedirs("json/seat")

for seat in seat_info:
    url = (
        "https://api.undi.info/election?"
        + f"seat={seat['state_code']}.p.{seat['seat_name'].replace(' ', '%20')}"
    )
    seat_name = seat["seat_name"]
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Retrieved data for {seat_name}")
        data = response.json()
        with open(f"json/seat/{seat_name}.json", "w") as jsonfile:
            json.dump(data, jsonfile, indent=4)
    else:
        print(f"Failed to retrieve data for {seat_name}")
