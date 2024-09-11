import pandas as pd
import re

# Load your CSV file
csv_file = 'glassdoor_dataengineer(501-1000)REMOTE.csv'  # Replace with the path to your file
df = pd.read_csv(csv_file)

# Function to convert relative time (like '24h', '30d') into a comparable number
def sort_key(relative_time_str):
    # Extract the number and the unit (h for hours, d for days)
    match = re.match(r'(\d+)([hd])', relative_time_str)
    if match:
        value, unit = match.groups()
        value = int(value)
        if unit == 'h':  # If it's in hours
            return value  # Hours come before days, so lower values are more recent
        elif unit == 'd':  # If it's in days
            return value * 24  # Convert days to hours for comparison
    return float('inf')  # Put invalid or unknown formats at the end

# Replace 'posted_date' with your actual column name
date_column = 'Job_PostedDate'  # Adjust this if necessary

# Sort the dataframe by the relative posted time using the custom sort key, with ascending=False to get latest first
df_sorted = df.sort_values(by=date_column, key=lambda col: col.apply(sort_key), ascending=True)

# Save the sorted dataframe to a new CSV file
df_sorted.to_csv('sorted_jobs_file.csv', index=False)

print("CSV file has been sorted by relative posted time (latest first) and saved as 'sorted_jobs_file.csv'.")
