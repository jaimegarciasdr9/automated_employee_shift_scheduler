# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:05:51 2023
@author: Jaime
#comment: This code will be executed every Friday to get the shifts for the following week
"""

import json
import requests
import pandas as pd
from pandas.tseries.offsets import BDay
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def get_next_week_dates():
    current_date = datetime.now()
    days_until_monday = (0 - current_date.weekday() + 7) % 7
    days_until_sunday = days_until_monday + 6

    start_date = current_date + timedelta(days=days_until_monday)
    end_date = current_date + timedelta(days=days_until_sunday)

    return start_date, end_date

# Get the start and end date of the next week
start_date, end_date = get_next_week_dates()

# Format dates
start_date_str = start_date.strftime('%Y/%m/%d')
end_date_str = end_date.strftime('%Y/%m/%d')

# Fetch token and other configurations from environment variables
token = os.getenv('API_TOKEN')
base_url = os.getenv('API_BASE_URL')
output_file_path = os.getenv('OUTPUT_FILE_PATH', 'shift_data_nextweek_with_business_day.xlsx')

url = f"{base_url}/labor/schedules/getShiftsByEmployee?start_date={start_date_str}&end_date={end_date_str}"

payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    'Api-version': '1.0'
}

# Make the API request
response = requests.request("GET", url, headers=headers, data=payload, files=files)

# Parse the response data
shift_data = json.loads(response.text)

data_list = []

# Extract relevant data from each shift entry
for shift in shift_data:
    shift_id = shift.get('shift_id', '')
    business_unit_id = shift.get('business_unit_id', '')
    business_unit = shift.get('business_unit', '')
    employee_id = shift.get('employee_id', '')
    employee_code = shift.get('employee_id', '')
    entry = shift.get('entry', '')
    exit_time = shift.get('exit', '')

    data_list.append({
        'Shift ID': shift_id,
        'Business Unit ID': business_unit_id,
        'Business Unit': business_unit,
        'Employee ID': employee_id,
        'Employee Code': employee_code,
        'Entry Time': entry,
        'Exit Time': exit_time
    })

# Create a DataFrame
df = pd.DataFrame(data_list)

# Add Business Day information to Entry and Exit times
df['Entry Business Day'] = pd.to_datetime(df['Entry Time']).apply(lambda x: x + BDay(0))
df['Exit Business Day'] = df['Entry Business Day']

# Format Business Days as strings
df['Business Day Start'] = df['Entry Business Day'].dt.strftime('%Y-%m-%d')
df.drop(['Entry Business Day'], axis=1, inplace=True)
df['Business Day End'] = df['Exit Business Day'].dt.strftime('%Y-%m-%d')
df.drop(['Exit Business Day'], axis=1, inplace=True)

# Export the DataFrame to Excel
df.to_excel(output_file_path, index=False)

print(f"Excel file created at: {output_file_path}")
