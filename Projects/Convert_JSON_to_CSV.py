############################################
# Author: Evan Whitfield 
# Date: 8/19/2025
# Purpose: To Convert JSON files from the StatsBomb data set to CSV files
#############################################

#imports
import pandas as pd
import json
import glob
import os

# Path to the folder containing JSON files - CHANGE ON DIFFERENT MACHINE
json_folder = r"C:\Users\edwhi\OneDrive\Desktop\Portfolio Projects\Soccer Predictor\open-data-master\data\events"


# Get all JSON files in the folder
json_files = glob.glob(os.path.join(json_folder, "*.json"))
total_files = len(json_files)
print(f"Found {total_files} JSON files to process.")

# Put all JSON data in a single list
all_events = []
for idx, f in enumerate(json_files, 1):
    print(f"Processing file {idx}/{total_files}: {os.path.basename(f)}")
    with open(f, encoding="utf-8") as infile:
        data = json.load(infile)
        df = pd.json_normalize(data)
        all_events.append(df)

#Convert List to CSV
if all_events:
    events_df = pd.concat(all_events, ignore_index=True)
    # Save to CSV
    events_df.to_csv("events.csv", index=False)
else:
    print("No JSON files found in the specified folder.")

#End Script
