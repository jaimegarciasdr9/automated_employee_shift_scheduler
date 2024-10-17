# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 11:05:51 2023
@author: Jaime
#comment: This code will be executed every friday in order to get the shifts for the following week
"""

import json
import requests
import pandas as pd
from pandas.tseries.offsets import BDay
from datetime import datetime, timedelta


def get_next_week_dates():
    current_date = datetime.now()
    days_until_monday = (0 - current_date.weekday() + 7) % 7
    days_until_sunday = days_until_monday + 6

    start_date = current_date + timedelta(days=days_until_monday)
    end_date = current_date + timedelta(days=days_until_sunday)

    return start_date, end_date


start_date, end_date = get_next_week_dates()

# Formatea las fechas
start_date_str = start_date.strftime('%Y/%m/%d')
end_date_str = end_date.strftime('%Y/%m/%d')

url = f"https://gotogir.com/wap/labor/schedules/getShiftsByEmployee?start_date={start_date_str}&end_date={end_date_str}"


token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjZCN0FDQzUyMDMwNUJGREI0RjcyNTJEQUVCMjE3N0NDMDkxRkFBRTEiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJhM3JNVWdNRnY5dFBjbExhNnlGM3pBa2ZxdUUifQ.eyJuYmYiOjE3MDEwNzg1NzksImV4cCI6MTc4NzQ3ODU3OSwiaXNzIjoiaHR0cHM6Ly9nb3RvZ2lyLmNvbS9sb2dpbiIsImF1ZCI6WyJodHRwczovL2dvdG9naXIuY29tL2xvZ2luL3Jlc291cmNlcyIsImFwaV93YXAiXSwiY2xpZW50X2lkIjoid2FwIiwic3ViIjoiMGUwN2FlZmYtY2M3NS00NzUwLWEyMmMtYzU0OTAwZmE2N2MyIiwiYXV0aF90aW1lIjoxNzAxMDc4NTc5LCJpZHAiOiJsb2NhbCIsInByZWZlcnJlZF91c2VybmFtZSI6ImZlcm5hbmRvLmxvcGV6QGxhbXVjY2Fjb21wYW55LmNvbSIsImVtYWlsIjoiZmVybmFuZG8ubG9wZXpAbGFtdWNjYWNvbXBhbnkuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBob25lX251bWJlciI6IjYxMCA1NyA3MSAwOCIsInBob25lX251bWJlcl92ZXJpZmllZCI6dHJ1ZSwicm9sZSI6WyJDbGltYSBMYWJvcmFsIiwiUGVyc29uYWwgZW4gVHVybm8iLCJUdXJub3MgUHJveWVjdGFkb3MiLCJQcmVzZW5jaWFfTGFib3JhbF9SZXZpc2FyIEluY2lkZW5jaWFzIl0sIkNMQUlNX1RZUEVfVVNFUl9JRCI6IjBlMDdhZWZmLWNjNzUtNDc1MC1hMjJjLWM1NDkwMGZhNjdjMiIsIkNMQUlNX1RZUEVfVVNFUl9OQU1FIjoiRmVybmFuZG8iLCJDTEFJTV9UWVBFX1VTRVJfTEFTVE5BTUVTIjoiTG9wZXogSGVybWlkYSIsIkNMQUlNX1RZUEVfVVNFUl9DVVJSRU5UX0NVTFRVUkUiOiJlbi1HQiIsIkNMQUlNX1RZUEVfR0lSX1VTRVJfSUQiOiJjYWQzNDFhOS1lMmM1LTQ3MmYtOGM5YS0xMzgwYmNiNGIxODUiLCJDTEFJTV9UWVBFX0RFRkFVTFRfT1BFUkFUT1JfSUQiOjExMzIsIkNMQUlNX1RZUEVfREVGQVVMVF9PUEVSQVRPUl9DT05ORUNUSU9OIjoiU2VydmVyPTE5Mi4xNjguMS4xMTM7UG9ydD01NDMyO1Bvb2xpbmc9dHJ1ZTtEYXRhYmFzZT1teWdpcl8xMTMyO1VzZXIgSWQ9YW50b25pbztQYXNzd29yZD1QODEwNTUzNztTc2xNb2RlPURpc2FibGU7TWluUG9vbFNpemU9MTtNYXhQb29sU2l6ZT00MDs7IiwiQ0xBSU1fVFlQRV9ERUZBVUxUX09QRVJBVE9SX0FQUExJQ0FUSU9OIjoibGFtdWNjYWNvbXBhbnkiLCJDTEFJTV9UWVBFX0RFRkFVTFRfT1BFUkFUT1JfTVlTUUxfQ1VMVFVSRSI6IkV1cm9wZS9NYWRyaWQiLCJDTEFJTV9UWVBFX0RFRkFVTFRfT1BFUkFUT1JfQ1VMVFVSRSI6ImVzLUVTIiwiQ0xBSU1fVFlQRV9ERUZBVUxUX09QRVJBVE9SX0NVUlJFTkNZIjoiRVVSIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImFwaV93YXAiXSwiYW1yIjpbInB3ZCJdfQ.PpH12x9_HxQZ_kdutE_QKTlzmKlq73J2zRhqPnd3tZL4txSj7umYtFEEBnYt2kNlPP1qZtfEu-pUa1dffYzbI7H9H_0M_ce0MjZW-qgpg788kAjRcIJ27WJ4u4Af3SE2rO1JOSn3FC9VLq7d6YVRh6idgMOqxP1agpj9QhYmZU0e17YNcTF998TA63JwNHw-LmX3_iTC4V-yHDBrG4Dyj1_kpCy5vElCxXCbcjLROEDEWJQCyCzWJEkAvHTZAOSeKRytwjs7ghPVeyiuiGzxXgm8klMn_5wq7E4tTdOMJ-_xQmPmt2xv7olifJGZ905t8xN1imuGZsiMJGrG0si0bw'

payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}',
    'Api-version': '1.0'
}

response = requests.request("GET", url, headers=headers, data=payload, files=files)

shift_data = json.loads(response.text)

data_list = []

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

df = pd.DataFrame(data_list)

df['Entry Business Day'] = pd.to_datetime(df['Entry Time']).apply(lambda x: x + BDay(0))
df['Exit Business Day'] = df['Entry Business Day']

df['Business Day Start'] = df['Entry Business Day'].dt.strftime('%Y-%m-%d')
df.drop(['Entry Business Day'], axis=1, inplace=True)
df['Business Day End'] = df['Exit Business Day'].dt.strftime('%Y-%m-%d')
df.drop(['Exit Business Day'], axis=1, inplace=True)

excel_file_path_with_business_day = 'C:/Users/nimer/OneDrive - Nimerya Data Science/Documentos - Nimerya Data Science/Lamucca/Personal/turnos/datos/shift_data_nextweek_with_business_day.xlsx'
df.to_excel(excel_file_path_with_business_day, index=False)

print(f"Archivo Excel creado en: {excel_file_path_with_business_day}")
