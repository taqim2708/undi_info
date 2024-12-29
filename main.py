import requests
import csv

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
        data.append(response.json())
    except requests.RequestException as e:
        print(f"Failed to fetch data from {url}: {e}")

# Write data to CSV
with open("api_data.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    # Write headers
    writer.writerow(["ge", "seat", "data"])
    # Write data
    for g, s, d in zip(ge * len(seat), seat * len(ge), data):
        writer.writerow([g, s, d])
