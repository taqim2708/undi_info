import json
import os


def update_turnout(file_path: str) -> None:
    with open(file_path, "r") as file:
        data = json.load(file)

    for election in data.values():
        total_votes = sum(candidate["Votes"] for candidate in election["candidates"])
        eligible_voters = int(election["info"]["EligibleVoters"])
        turnout_percent = (
            (total_votes / eligible_voters) * 100 if eligible_voters > 0 else 0
        )

        election["info"]["ValidVoteCount"] = str(total_votes)
        election["info"]["ValidVotePercent"] = f"{turnout_percent:.2f}"

    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Update all JSON files in the json/seat directory
seat_directory = "json/seat"
for filename in os.listdir(seat_directory):
    if filename.endswith(".json"):
        update_turnout(os.path.join(seat_directory, filename))
