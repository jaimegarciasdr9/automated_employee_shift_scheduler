# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:04:23 2023

@author: Dani
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Get sensitive data from environment variables
username = os.getenv('API_USERNAME')
password = os.getenv('API_PASSWORD')
client_id = os.getenv('API_CLIENT_ID', 'wap')
client_secret = os.getenv('API_CLIENT_SECRET', 'secret')

url = "https://gotogir.com/login/connect/token"

# Prepare the payload
payload = {
    'grant_type': 'password',
    'username': username,
    'password': password,
    'client_id': client_id,
    'client_secret': client_secret
}

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Make the POST request
response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
