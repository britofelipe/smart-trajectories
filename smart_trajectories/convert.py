import pandas as pd
import os
from datetime import datetime
import ast

# Reads the trajectories from a text file and write the processed data into a CSV file 
def txt_to_csv(txt_filename, csv_filename):
    if not os.path.exists(txt_filename):
        print("Text file not found.")
        return
    
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    df_list = []
    for line in lines:
        parts = line.strip().split(', ')

        identifier = float(parts[0])
        category = float(parts[1])
        start_time = float(parts[2])
        end_time = float(parts[3])

        # Points array
        points_string = ', '.join(parts[4:])
        points = ast.literal_eval(points_string)

        time_interval = (end_time - start_time) / len(points)

        for i, point in enumerate(points):
            timestamp = start_time + i * time_interval
            x, y = point
            df_list.append([identifier, category, timestamp, x, y])

    df = pd.DataFrame(df_list, columns=['identifier', 'category', 'timestamp', 'x', 'y'])
    df.to_csv(csv_filename, index=False)

def txt_to_csv_datetime(txt_filename, csv_filename):
    if not os.path.exists(txt_filename):
        print("Text file not found.")
        return
    
    with open(txt_filename, 'r') as f:
        lines = f.readlines()

    df_list = []
    for line in lines:
        parts = line.strip().split(', ')

        identifier = int(parts[0])
        category = int(parts[1])
        start_time = datetime.strptime(parts[2], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.strptime(parts[3], "%Y-%m-%d %H:%M:%S.%f")

        # Points array
        points_string = ', '.join(parts[4:])
        points = ast.literal_eval(points_string)

        total_seconds = (end_time - start_time).total_seconds()
        time_interval = total_seconds / len(points)

        for i, point in enumerate(points):
            timestamp = (start_time + pd.Timedelta(seconds=i * time_interval)).timestamp()
            x, y = point
            df_list.append([identifier, category, timestamp, x, y])

    df = pd.DataFrame(df_list, columns=['identifier', 'category', 'timestamp', 'x', 'y'])
    df.to_csv(csv_filename, index=False)