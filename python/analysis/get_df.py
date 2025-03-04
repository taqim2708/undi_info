import os
import json
import pandas as pd
import random
import seaborn as sns
from pandas import Index, MultiIndex


def get_dataframe() -> pd.DataFrame:
    # Directory where JSON files are stored
    DATA_DIR = "json/seats"

    # Load all JSON files
    election_results = []

    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".json"):
            with open(os.path.join(DATA_DIR, filename), "r", encoding="utf-8") as file:
                data = json.load(file)
                election_results.append(data)

    # Convert to structured DataFrame
    records = []

    for seat in election_results:
        seat_name = list(seat.values())[0]["SeatName"]

        for year_key, details in seat.items():
            year = details["year"]
            valid_votes = details["info"]["ValidVoteCount"]
            turnout = details["info"]["ValidVotePercent"]

            for candidate in details["candidates"]:
                records.append({
                    "Year": year,
                    "Seat": seat_name,
                    "Party": candidate["Party"],
                    "Candidate": candidate["Name"],
                    "Votes": candidate["Votes"],
                    "ValidVotes": valid_votes,
                    "Turnout": turnout
                })

    return pd.DataFrame(records)


def get_palette(top_parties: Index | MultiIndex) -> dict:
    # Define custom colors for specific parties
    party_colors = {
        "PKR": "blue",
        "PAS": "green",
        "UMNO": "red",
    }

    # Generate random colors for parties not in the predefined list
    all_colors = sns.color_palette("hsv", len(top_parties))
    random.shuffle(all_colors)
    for party in top_parties:
        if party not in party_colors:
            party_colors[party] = all_colors.pop()
    return party_colors
