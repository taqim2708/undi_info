import csv
import json

# Read input data from CSV
input_file = "api_data.csv"
input_data = []

with open(input_file, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        input_data.append(row)

# Convert and flatten the JSON
flattened_data = []
for row in input_data:
    ge = row["ge"]
    seat = row["seat"]
    data = json.loads(
        row["data"].replace("'", '"')
    )  # Convert the JSON string to a Python dictionary

    for key, value in data.items():
        for party, count in value.items():
            flattened_data.append(
                {"ge": ge, "seat": seat, "region": key, "party": party, "count": count}
            )

# Write to a new CSV
output_file = "flattened_data.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=["ge", "seat", "region", "party", "count"])
    writer.writeheader()
    writer.writerows(flattened_data)

print(f"Flattened data has been written to {output_file}.")
