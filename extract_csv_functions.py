from datetime import datetime as datetime
import re
import pandas as pd

def vid_extract_timestamp(file_name, timestamp_pattern):
    # Use re.search to find the pattern in the file name
    match = re.search(eval(timestamp_pattern), file_name)

    # Check if a match is found
    if match:
        timestamp_str = match.group(1)
        # Convert the string timestamp to a datetime object
        timestamp_dt = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        
        
        return timestamp_dt
    else:
        return None
    
def rt_extract_timestamp(file_name, timestamp_pattern):
    df = pd.read_csv(file_name, nrows=4)
    # print(df)
    # Extract the text from the specified cell
    cell_text = df.iloc[1,0]
    print(cell_text)
    # Check if the expected text is present in the cell
        # Use regular expression to extract the timestamp from the cell
    match = re.search(eval(timestamp_pattern), cell_text)
    if match:
        timestamp_str = match.group(1)
        # Convert the string timestamp to a datetime object
        timestamp_dt = datetime.strptime(timestamp_str, "%m/%d/%Y %I:%M:%S %p")        
        
        return timestamp_dt
    return None

def convert_RT_speed20Hz(file_name):
    df = pd.read_csv(file_name, skiprows=5, header=0, index_col=False)
    df = df[['time [s]', 'Speed [kph]']]

    # Convert 'time' to 20Hz frequency by averaging every 5 consecutive rows
    df['time [s]'] = pd.to_datetime(df['time [s]'], unit='s')
    df = df.resample('50L', on='time [s]').mean().reset_index()

    # Assuming 'E' is the column you want to convert to 20Hz frequency by averaging every 5 consecutive rows
    # df['Speed [kph]'] = df['Speed [kph]'].rolling(5).mean()

    # Drop any NaN values resulting from the rolling mean operation
    # df = df.dropna()

    # Reset index
    # df = df.reset_index(drop=True)

    # Print the resulting DataFrame
    print(df.head())
    return df

def combine_pred_rt_speeds(convert_rt_20hz, pred_file, start_difference):
    pred_df = pd.read_csv(pred_file, header=None, names=['predicted_speed'])
    start_difference = int(start_difference*20)
    df = convert_rt_20hz

    if start_difference>0:
        predicted_speed_df = pred_df[start_difference:min(len(convert_rt_20hz)+start_difference, len(pred_df))].reset_index()
        # Pad predicted_speed_df with zeros at the beginning
        rt_speed_df = convert_rt_20hz[:min(len(convert_rt_20hz), len(pred_df)-start_difference)].reset_index()
    else:
        predicted_speed_df = pred_df[:min(len(convert_rt_20hz), len(pred_df)-start_difference)].reset_index()
        # Pad predicted_speed_df with zeros at the beginning
        rt_speed_df = convert_rt_20hz[-start_difference:min(len(convert_rt_20hz+start_difference), len(pred_df))].reset_index()

    df = rt_speed_df
    # Combine the two DataFrames
    df['predicted_speed'] = predicted_speed_df['predicted_speed']
    df = df.resample('1S', on='time [s]').max()

    # # Fill NaN values with 0
    # df['predicted_speed'] = df['predicted_speed'].fillna(0)

    # Reset index
    # df = df.reset_index(drop=True)

    # Print the resulting DataFrame
    print(df.head())
    return df

