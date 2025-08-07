##########################
# Author: Evan Whitfield
# Date: 08/06/2025 
# Description: Data Extraction and Analysis Script
###########################

#needed imports
from zipfile import ZipFile
import os
import pandas as pd

# Define the path to the uploaded ZIP file
zip_path = "health-risk-analysis/data/MMSA22_ASC.zip"
extract_dir = "health-risk-analysis/data/"

# Extract the ZIP file
with ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# List extracted files
extracted_files = os.listdir(extract_dir)
extracted_files

# Define the file path
asc_file_path = os.path.join(extract_dir, 'MMSA22.ASC')

# Define colspecs and names from the layout data you provided
colspecs = [
    (0, 4), (4, 14), (14, 15), (15, 16), (16, 17), (17, 18), (18, 19), (19, 20),
    (20, 21), (21, 22), (22, 23), (23, 25), (25, 26), (26, 27), (27, 29), (29, 31),
    (31, 33), (33, 35), (35, 36), (36, 37), (37, 38), (38, 39), (39, 40), (40, 42),
    (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 48), (48, 49), (49, 50),
    (50, 51), (51, 52), (52, 53), (53, 54), (54, 55), (55, 57), (57, 85), (85, 87),
    (87, 88), (88, 89), (89, 90), (90, 91), (91, 92), (92, 93), (93, 94), (94, 95),
    (95, 96), (96, 98), (98, 100), (100, 101), (101, 105), (105, 109), (109, 110),
    (110, 111), (111, 112), (112, 113), (113, 114), (114, 115), (115, 116), (116, 117),
    (117, 118), (118, 119), (119, 120), (120, 121), (121, 122), (122, 123), (123, 124),
    (124, 125), (125, 126), (126, 127), (127, 128), (128, 129)
]

colnames = [
    'DISPCODE', 'SEQNO', 'STATERE1', 'CELPHON1', 'LADULT1', 'COLGSEX1', 'LANDSEX1', 'RESPSLCT',
    'SAFETIME', 'CADULT1', 'CELLSEX1', 'HHADULT', 'SEXVAR', 'GENHLTH', 'PHYSHLTH', 'MENTHLTH',
    'POORHLTH', 'PRIMINSR', 'PERSDOC3', 'MEDCOST1', 'CHECKUP1', 'EXERANY2', 'SLEPTIM1', 'LASTDEN4',
    'RMVTETH4', 'CVDINFR4', 'CVDCRHD4', 'CVDSTRK3', 'ASTHMA3', 'ASTHNOW', 'CHCSCNC1', 'CHCOCNC1',
    'CHCCOPD3', 'ADDEPEV3', 'CHCKDNY2', 'HAVARTH4', 'DIABETE4', 'DIABAGE4', 'MRACE2', 'ORACE4',
    'MARITAL', 'EDUCA', 'RENTHOM1', 'NUMHHOL4', 'NUMPHON4', 'CPDEMO1C', 'VETERAN3', 'EMPLOY1',
    'CHILDREN', 'INCOME3', 'PREGNANT', 'WEIGHT2', 'HEIGHT3', 'DEAF', 'BLIND', 'DECIDE', 'DIFFWALK',
    'DIFFDRES', 'DIFFALON', 'HADMAM', 'HOWLONG', 'CERVSCRN', 'CRVCLCNC', 'CRVCLPAP', 'CRVCLHPV',
    'HADHYST2', 'HADSIGM4', 'COLNSIGM', 'COLNTES1', 'SIGMTES1', 'LASTSIG4', 'COLNCNCR', 'VIRCOLO1',
    'VCLNTES2'
]

# Read a sample of the file to verify formatting
df_sample = pd.read_fwf(asc_file_path, colspecs=colspecs, names=colnames, nrows=1000)
df_sample.head()

variables_of_interest = [
    "STATERE1",     # state
    "BMI5",         # body mass index ×100
    "WEIGHT2",      # weight (lbs)
    "HEIGHT3",      # height (in)
    "EXERANY2",     # any exercise
    "GENHLTH",      # general health
    "SLEPTIM1",     # hours of sleep
    "MENTHLTH",     # days mental health was poor
    "ADDEPEV3",     # diagnosed depression
    "DECIDE",       # difficulty concentrating/deciding
]

# Filter the DataFrame to include only the variables of interest
df_filtered = df_sample[variables_of_interest]

# Replace invalid/missing codes per BRFSS codebook (you may need to adjust based on documentation)
df['WEIGHT2'] = pd.to_numeric(df['WEIGHT2'], errors='coerce')
df['HEIGHT3'] = pd.to_numeric(df['HEIGHT3'], errors='coerce')

# Set invalid values to NaN
df.loc[df['WEIGHT2'] > 9998, 'WEIGHT2'] = None  # 9999 = Refused / 7777 = Don't know
df.loc[df['HEIGHT3'] > 9998, 'HEIGHT3'] = None

# Calculate BMI
df['BMI'] = (df['WEIGHT2'] / (df['HEIGHT3'] ** 2)) * 703

# Categorize BMI
def bmi_category(bmi):
    if pd.isna(bmi):
        return None
    elif bmi < 18.5:
        return 'Underweight'
    elif bmi < 25:
        return 'Normal'
    elif bmi < 30:
        return 'Overweight'
    else:
        return 'Obese'

df['BMI_Category'] = df['BMI'].apply(bmi_category)

# Preview results
print(df[['WEIGHT2', 'HEIGHT3', 'BMI', 'BMI_Category']].head())

# Save the filtered DataFrame to a new CSV file
output_csv_path = os.path.join(extract_dir, 'filtered_data.csv')

df_filtered.to_csv(output_csv_path, index=False)
print(f"Filtered data saved to {output_csv_path}")

# Display the first few rows of the filtered DataFrame
print(df_filtered.head())

# Additional analysis or processing can be done here

# End of script

