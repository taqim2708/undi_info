import requests
import json

ge = [
    "prn2023",
    "sarawak2021",
    "melaka2021",
    "sabah2020",
    "sarawak2016",
    "ge15",
    "ge14",
    "ge13",
    "ge12",
    "ge11",
]
seat = ["state", "parliament"]

state_codes = ["kd" "pn" "ke" "tr" "sl" "ns" "sw" "mk" "sb" "pl" "pr" "ph" "wp" "jh"]

urls = [
    f"https://api.undi.info/party_summary?ge={g}&seat={s}" for g in ge for s in seat
]

# List to store the data
data = []

# Fetch data from each URL
for url in urls:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Fetching data from {url}")
        data.append({
            "ge": url.split("ge=")[1].split("&")[0],
            "seat": url.split("seat=")[1],
            "data": response.json()
        })
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")

# Write data to JSON file
with open("json/api_data.json", mode="w") as file:
    json.dump(data, file, indent=4)
