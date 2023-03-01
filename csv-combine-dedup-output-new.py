import os
import pandas as pd

# Get a list of all CSV files in the current directory
csv_files = [file for file in os.listdir('.') if file.endswith('.csv')]

# Combine all CSV files into a single DataFrame
df = pd.concat([pd.read_csv(file) for file in csv_files])

# Deduplicate the DataFrame
df = df.drop_duplicates()

# Write the deduplicated DataFrame to a final CSV file
df.to_csv('final.csv', index=False)
