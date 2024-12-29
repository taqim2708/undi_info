import pandas as pd

# Load data from CSV file
file_path = "flattened_data.csv"
df = pd.read_csv(file_path)

# Extract state codes from the 'region' column
df["state_code"] = df["region"].str.split("-").str[0]

# Get unique state codes
unique_state_codes = df["state_code"].unique()

# Display the unique state codes
print("Unique state codes:", unique_state_codes)
