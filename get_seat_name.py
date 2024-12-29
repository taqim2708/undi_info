import requests
import csv

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

urls = [
    f"https://api.undi.info/listing?negeri={state_code}&ge=ge12&seat=parliament"
    for state_code in state_codes
]

# List to store the seat names
seat_names = []

for url in urls:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        print(f"Fetching data from {url}")
        data = response.json()
        seats = data.get("seats", [])
        if not seats:
            print(f"\033[91mNo seats found for {url}\033[0m")
        for seat in seats:
            seat_names.append([seat.get("name", "N/A")])
    except requests.RequestException as e:
        print(f"\033[91mFailed to retrieve data from {url}: {e}\033[0m")

# Write the seat names to a CSV file
with open("seat_name.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Seat Name"])
    writer.writerows(seat_names)

print("Seat names have been written to seat_name.csv")
