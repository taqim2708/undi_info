import matplotlib.pyplot as plt
import seaborn as sns
from python.analysis.get_df import get_dataframe, get_palette

df = get_dataframe()

# Count seats won per party per election
seat_wins = df.groupby(["Year", "Party"])["Seat"].count().reset_index()
seat_wins.rename(columns={"Seat": "Seats Won"}, inplace=True)

# Calculate total seats won by each party
total_seats = seat_wins.groupby("Party")["Seats Won"].sum().reset_index()
n = 15
top_n_parties = total_seats.nlargest(n, "Seats Won")["Party"]

# Filter seat_wins to include only top n parties
seat_wins_top_n = seat_wins[seat_wins["Party"].isin(top_n_parties)]

# Visualize seat distribution
plt.figure(figsize=(12, 6))
sns.barplot(data=seat_wins_top_n, x="Year", y="Seats Won", hue="Party", palette=get_palette(top_n_parties))
plt.xlabel("Election Year")
plt.ylabel("Number of Seats Won")
plt.title("Seat Distribution by Top n Parties Across Elections")
plt.legend(title="Party")
plt.show()
