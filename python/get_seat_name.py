import requests
import json

state_codes = [
    "kd",
    "pn",
    "ke",
    "tr",
    "sl",
    "ns",
    "sw",
    "mk",
    "sb",
    "pl",
    "pr",
    "ph",
    "wp",
    "jh",
]

# List to store the seat names
seat_names = []

for state_code in state_codes:
    url = f"https://api.undi.info/listing?negeri={state_code}&ge=ge15&seat=parliament"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Fetching data from {url}")
        data = response.json()
        seats = data.get("seats", [])
        if not seats:
            print(f"\033[91mNo seats found for {url}\033[0m")
        for seat in seats:
            seat_names.append({
                "pcode": seat.get("pcode", "N/A"),
                "seat_name": seat.get("name", "N/A"),
                "state_code": state_code,
                })
    except requests.RequestException as e:
        print(f"\033[91mFailed to retrieve data from {url}: {e}\033[0m")

# Write the seat names to a JSON file
with open("json/seat_info.json", mode="w", encoding="utf-8") as file:
    json.dump(seat_names, file, ensure_ascii=False, indent=4)

print("Seat names have been written to json/seat_info.json")
