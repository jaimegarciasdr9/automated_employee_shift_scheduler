# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:04:23 2023

@author: Dani
"""

import requests

url = "https://gotogir.com/login/connect/token"

payload = {'grant_type': 'password',
'username': 'fernando.lopez@lamuccacompany.com',
'password': 'Lamucca.1',
'client_id': 'wap',
'client_secret': 'secret'}
files=[

]
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)