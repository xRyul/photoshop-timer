import pandas as pd
import glob

# Get a list of all CSV files in the 'logs' subfolder
files = glob.glob('/Users/dan00477/Desktop/photoshop-timer/logs/*.csv')

# Initialize an empty DataFrame to store all data
all_data = pd.DataFrame()

# Loop through all files and append their data to the DataFrame
for file in files:
    df = pd.read_csv(file, skiprows=1)
    df.columns = ['Department', 'Filename', 'Execution Time', 'History Steps']
    df['Execution Time'] = pd.to_timedelta(df['Execution Time']).dt.total_seconds()
    all_data = pd.concat([all_data, df], ignore_index=True)

# Group by Department and calculate the mean of Execution Time and History Steps
grouped = all_data.groupby('Department').agg({'Execution Time': 'mean', 'History Steps': 'mean'}).reset_index()

# Convert 'Department' to int
grouped['Department'] = grouped['Department'].astype(int)

# Check if the output file already exists
try:
    df_out = pd.read_csv('/Users/dan00477/Desktop/photoshop-timer/average_data.csv')
    # Convert 'Department' to int
    df_out['Department'] = df_out['Department'].astype(int)
except FileNotFoundError:
    df_out = pd.DataFrame(columns=['Department', 'Average Execution Time', 'Average History Steps', 'Images Processed per Hour'])

# Update the output DataFrame with the new averages
for index, row in grouped.iterrows():
    if row['Department'] in df_out['Department'].values:
        df_out.loc[df_out['Department'] == row['Department'], 'Average Execution Time'] = row['Execution Time']
        df_out.loc[df_out['Department'] == row['Department'], 'Average History Steps'] = row['History Steps']
        df_out.loc[df_out['Department'] == row['Department'], 'Images Processed per Hour'] = 3600 / row['Execution Time']
    else:
        new_row = pd.DataFrame({'Department': [row['Department']], 'Average Execution Time': [row['Execution Time']], 'Average History Steps': [row['History Steps']], 'Images Processed per Hour': [3600 / row['Execution Time']]})
        df_out = pd.concat([df_out, new_row], ignore_index=True)

# Save the output DataFrame to a CSV file
df_out.to_csv('/Users/dan00477/Desktop/photoshop-timer/average_data.csv', index=False)
