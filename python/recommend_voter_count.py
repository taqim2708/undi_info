import json
import os

"""
SPlit between East Malaysia and Peninsular Malaysia
"""
EAST_MY = ["sw", "sb"]
PENINSULAR_MY = [
    "kd",
    "pn",
    "ke",
    "tr",
    "sl",
    "ns",
    "mk",
    "pl",
    "pr",
    "ph",
    "wp",
    "jh",
]


def adjust_seats(total_voters_and_seats: dict[str, dict[str, int]]) -> dict[str, int]:
    total_voters = sum(
        info["eligible_voters"] for _, info in total_voters_and_seats.items()
    )
    total_seats = sum(info["seats"] for _, info in total_voters_and_seats.items())

    # Compute ideal seats per state based on voter proportion
    ideal_seats = {
        state: round((info["eligible_voters"] / total_voters) * total_seats)
        for state, info in total_voters_and_seats.items()
    }

    # Adjust to maintain total seat count
    seat_difference = total_seats - sum(ideal_seats.values())
    sorted_states = sorted(
        total_voters_and_seats.keys(),
        key=lambda s: (total_voters_and_seats[s]["eligible_voters"] / total_voters_and_seats[s]["seats"]),
        reverse=True,
    )

    for i in range(abs(seat_difference)):
        if seat_difference > 0:
            ideal_seats[
                sorted_states[-(i + 1)]
            ] -= 1  # Reduce seats in states with lower voter-to-seat ratio
        elif seat_difference < 0:
            ideal_seats[
                sorted_states[i]
            ] += 1  # Increase seats in states with higher voter-to-seat ratio

    return {
        state: ideal_seats[state] - total_voters_and_seats[state]["seats"]
        for state in total_voters_and_seats.keys()
    }


def split_dict(d: dict[str, dict], arr1: list, arr2: list) -> tuple[dict, dict]:
    d1 = {k: v for k, v in d.items() if k.lower() in arr1}
    d2 = {k: v for k, v in d.items() if k.lower() in arr2}
    return d1, d2


def get_total_voters_and_seats(directory: str) -> dict:
    total_voters_and_seats = {}

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as file:
                data = json.load(file)
                if "2022-GE" in data:
                    state_code = data["2022-GE"]["State"]
                    eligible_voters = int(data["2022-GE"]["info"]["EligibleVoters"])
                    if state_code not in total_voters_and_seats:
                        total_voters_and_seats[state_code] = {
                            "eligible_voters": 0,
                            "seats": 0,
                        }
                    total_voters_and_seats[state_code][
                        "eligible_voters"
                    ] += eligible_voters
                    total_voters_and_seats[state_code]["seats"] += 1

    return total_voters_and_seats


def get_highest_and_lowest_voters(directory: str) -> dict:
    east_voters = []
    peninsular_voters = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            eligible_voters, state_code = get_eligible_voters_and_state(file_path)

            if state_code.lower() in EAST_MY:
                east_voters.append(eligible_voters)
            elif state_code.lower() in PENINSULAR_MY:
                peninsular_voters.append(eligible_voters)

    highest_lowest_voters = {
        "east": {
            "highest": max(east_voters) if east_voters else 0,
            "lowest": min(east_voters) if east_voters else 0,
        },
        "peninsular": {
            "highest": max(peninsular_voters) if peninsular_voters else 0,
            "lowest": min(peninsular_voters) if peninsular_voters else 0,
        },
    }

    return highest_lowest_voters


def get_eligible_voters_and_state(file_path: str) -> tuple[int, str]:
    with open(file_path, "r") as file:
        data = json.load(file)
        if "2022-GE" in data:
            eligible_voters = int(data["2022-GE"]["info"]["EligibleVoters"])
            state_code = data["2022-GE"]["State"]
            return eligible_voters, state_code
        raise ValueError(f"2022-GE not found in {file_path}")
    raise ValueError(f"Eligible voters not found in {file_path}")


def calculate_average_voters(directory: str) -> tuple[float, float]:
    east_voters = []
    peninsular_voters = []

    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            eligible_voters, state_code = get_eligible_voters_and_state(file_path)

            if state_code.lower() in EAST_MY:
                east_voters.append(eligible_voters)
            elif state_code.lower() in PENINSULAR_MY:
                peninsular_voters.append(eligible_voters)

    avg_east_voters = sum(east_voters) / len(east_voters) if east_voters else 0
    avg_peninsular_voters = (
        sum(peninsular_voters) / len(peninsular_voters) if peninsular_voters else 0
    )

    return avg_east_voters, avg_peninsular_voters


# Example usage:
directory = "json/seat"
avg_east_voters, avg_peninsular_voters = calculate_average_voters(directory)
print(f"Average Eligible Voters in East Malaysia: {avg_east_voters}")
print(f"Average Eligible Voters in Peninsular Malaysia: {avg_peninsular_voters}")
print(get_highest_and_lowest_voters(directory))
east, peninsular = split_dict(get_total_voters_and_seats(directory), EAST_MY, PENINSULAR_MY)
print(adjust_seats(east))
print(adjust_seats(peninsular))
