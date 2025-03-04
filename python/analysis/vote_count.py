import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from python.analysis.get_df import get_dataframe, get_palette

df = get_dataframe()
# Aggregate votes by year & party
party_votes = df.groupby(["Year", "Party"])["Votes"].sum().reset_index()

# Show snapshot of DataFrame
print(party_votes.head())

# Plot vote share trends
# Get top n parties by total votes across all years
n = 10
top_parties = party_votes.groupby("Party")["Votes"].sum().nlargest(n).index

# Filter DataFrame to include only top n parties
top_party_votes = party_votes[party_votes["Party"].isin(top_parties)]

# Calculate total votes per year
total_votes_per_year = party_votes.groupby("Year")["Votes"].sum().reset_index()
total_votes_per_year = total_votes_per_year.rename(columns={"Votes": "TotalVotes"})

# Merge to get total votes in the same DataFrame
top_party_votes = pd.merge(top_party_votes, total_votes_per_year, on="Year")

# Calculate vote share percentage
top_party_votes["VoteSharePercent"] = (
    top_party_votes["Votes"] / top_party_votes["TotalVotes"]
) * 100

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=top_party_votes,
    x="Year",
    y="VoteSharePercent",
    hue="Party",
    marker="o",
    palette=get_palette(top_parties),
)
plt.xlabel("Election Year")
plt.ylabel("Vote Share (%)")
plt.title("Top 10 Party Vote Share Over Elections")
plt.legend(title="Party")
plt.grid(True)
plt.show()
