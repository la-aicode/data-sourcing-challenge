import requests
import time
from dotenv import load_dotenv
import os
import pandas as pd
import json
import os
from datetime import datetime
## Load the NASA_API_KEY from the env file
load_dotenv()
NASA_API_KEY = os.getenv('NASA_API_KEY')
# Request (5 points)
base_url = "https://api.nasa.gov/DONKI/"
specifier = "CME"
start_date = "2024-01-01"
end_date = "2024-05-01"
api_key = NASA_API_KEY  # Replace with your NASA API key

# Construct the query URL
query_url_CME = f"{base_url}{specifier}?startDate={start_date}&endDate={end_date}&api_key={api_key}"

# Make the GET request and store the JSON data
cme_response = requests.get(query_url_CME)
if cme_response.status_code == 200:
    cme_json = cme_response.json()
else:
    raise Exception(f"Failed to fetch data: {cme_response.status_code}")

# Preview the first results with json.dumps
print(json.dumps(cme_json[:1], indent=4))

# Convert cme_json to a Pandas DataFrame
cme_df = pd.DataFrame(cme_json)

# Preparation for loop 
expanded_rows = []  # Create an empty list

# Inside the cme.index for loop 
for index, row in cme_df.iterrows():  # Loop through cme.index list
    # Extract relevant columns
    activityID = row.get('activityID', None)
    startTime = row.get('startTime', None)
    linkedEvents = row.get('linkedEvents', [])


  # Ensure linkedEvents is a list; if None, use an empty list
    if linkedEvents is None:
        linkedEvents = []
        
    # Inner loop to iterate through linkedEvents
    for event in linkedEvents:
        expanded_rows.append({
            "activityID": activityID,
            "startTime": startTime,
            "linkedEventActivityID": event.get('activityID', None)
        })

# Create a new DataFrame from expanded_rows
expanded_df = pd.DataFrame(expanded_rows)

# Function extract_activityID_from_dict 
def extract_activityID_from_dict(event_dict):
    """
    Extracts the 'activityID' from a dictionary if it exists.
    """
    try:
        return event_dict.get('activityID')
    except AttributeError as e:
        print(f"Error: {e}")
        return None

# Apply the function with lambda
expanded_df['GST_ActivityID'] = expanded_df['linkedEventActivityID'].apply(lambda x: extract_activityID_from_dict({'activityID': x}))

# Cleaning (5 points)
# Convert GST_ActivityID to string
expanded_df['GST_ActivityID'] = expanded_df['GST_ActivityID'].astype(str)

# Convert startTime to datetime and rename it
expanded_df['startTime_CME'] = pd.to_datetime(expanded_df['startTime'], errors='coerce')

# Rename activityID to cmeID
expanded_df.rename(columns={'activityID': 'cmeID'}, inplace=True)

# Drop unnecessary columns
expanded_df.drop(columns=['linkedEventActivityID', 'startTime'], inplace=True)

# Filter rows where GST_ActivityID contains 'GST'
filtered_df = expanded_df[expanded_df['GST_ActivityID'].str.contains('GST', na=False)]

# Verify the final DataFrame
print("Final DataFrame:")
print(filtered_df.head())

#Now get GST Data

# Set API parameters for GST
GST_base_url = "https://api.nasa.gov/DONKI/"
specifier = "GST"
start_date = "2024-01-01"
end_date = "2024-05-01"
api_key = NASA_API_KEY  # Replace with your NASA API key

# Construct the GST URL
query_url_GST = f"{GST_base_url}{specifier}?startDate={start_date}&endDate={end_date}&api_key={api_key}"

# Make the GET request and store the JSON data
gst_response = requests.get(query_url_GST)
if gst_response.status_code == 200:
    gst_json = gst_response.json()
else:
    raise Exception(f"Failed to fetch GST data: {gst_response.status_code}")

# Preview the first results with json.dumps
print(json.dumps(gst_json[:1], indent=4))

# Convert gst_json to a Pandas DataFrame and keep specific columns
gst_df = pd.DataFrame(gst_json)
gst_df = gst_df[['activityID', 'startTime', 'linkedEvents']]

# Remove rows with missing 'linkedEvents'
gst_df = gst_df[gst_df['linkedEvents'].notna()]

# Spread multiple events in linkedEvents into individual rows
gst_df = gst_df.explode('linkedEvents')

# Apply the extract_activityID_from_dict function to extract activityID from linkedEvents
gst_df.loc[:, 'CME_ActivityID'] = gst_df['linkedEvents'].apply(
    lambda x: extract_activityID_from_dict(x) if isinstance(x, dict) else None
)

# Remove rows with missing 'CME_ActivityID'
gst_df = gst_df[gst_df['CME_ActivityID'].notna()]

# Convert gstID to string and startTime to datetime format
gst_df['activityID'] = gst_df['activityID'].astype(str)
gst_df['startTime'] = pd.to_datetime(gst_df['startTime'], errors='coerce')

# Rename columns
gst_df.rename(columns={'startTime': 'startTime_GST', 'activityID': 'gstID'}, inplace=True)

# Drop the linkedEvents column
gst_df.drop(columns=['linkedEvents'], inplace=True)

# Filter rows where CME_ActivityID contains 'CME'
gst_df = gst_df[gst_df['CME_ActivityID'].str.contains('CME', na=False)]

# Verify the final DataFrame
print("Final GST DataFrame:")
print(gst_df.head())

# Merge the two DataFrames on their respective ID columns
merged_df = pd.merge(
    gst_df,
    filtered_df,
    left_on=['gstID', 'CME_ActivityID'],
    right_on=['GST_ActivityID', 'cmeID']
)

# Verify the number of rows in the merged DataFrame
print(f"Number of rows in the merged DataFrame: {len(merged_df)}")
print(f"Number of rows in GST DataFrame: {len(gst_df)}")
print(f"Number of rows in CME DataFrame: {len(filtered_df)}")

# Compute the time difference between startTime_GST and startTime_CME
merged_df['timeDiff'] = (merged_df['startTime_GST'] - merged_df['startTime_CME']).dt.total_seconds()

# Use describe() to compute mean and median time
time_diff_stats = merged_df['timeDiff'].describe()
mean_time_diff = time_diff_stats['mean']
median_time_diff = merged_df['timeDiff'].median()

print(f"Mean time difference: {mean_time_diff} seconds")
print(f"Median time difference: {median_time_diff} seconds")

# Display time difference statistics
print("Time difference statistics:")
print(time_diff_stats)

# Export the merged and cleaned data to a CSV file
merged_df.to_csv('merged_cme_gst_data.csv', index=False)

print("Data exported to 'merged_cme_gst_data.csv'")

