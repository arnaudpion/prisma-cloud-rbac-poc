#!/usr/bin/env python3

import os
import requests
import json


### Credentials for API Authentication ###
username = os.environ.get('PC_PY_IDENTITY')  # Access Key in Prisma Cloud
password = os.environ.get('PC_PY_SECRET')    # Secret Key in Prisma Cloud


### API Endpoint ###
url = os.environ.get('PC_PY_URL')  # Prisma Cloud API URL - Check https://pan.dev/prisma-cloud/api/cspm/api-urls/


### Other Variables - Copy Paste the Output of the 01_create_rbac.py Script Here ###
account_prefix = "test"
account_list = []
account_group_list = []
role_list = []


### Login - Retrieve JWT for API Authentication ###
payload = json.dumps({
    'username': username,
    'password': password
    })

headers = {
  'Content-Type': 'application/json; charset=UTF-8',
  'Accept': 'application/json; charset=UTF-8'
}

response = requests.request("POST", url+"/login", headers=headers, data=payload)
json_response = json.loads(response.content)
auth_jwt = json_response.get('token')


### Clean Up - Delete Roles Previously Created ###
print("\n+++ CLEAN UP +++\n")

for role in role_list:
    api_url = url + "/user/role/" + role

    print("DELETE ROLE " + role + "\n")

    payload={}
    headers = {
        'Content-Type': 'application/json',
        'x-redlock-auth': auth_jwt
    }

    response = requests.request("DELETE", api_url, headers=headers, data=payload)


### Clean Up - Delete Account Groups Previously Created (Need to Empty Them First) ###

for account_group in account_group_list:
    api_url = url + "/cloud/group/" + account_group

    print("EMPTY ACCOUNT GROUP " + account_group)
    
    payload = json.dumps({
        "accountIds": [],
        "name": "TO BE DELETED"
    })
    headers = {
        'Content-Type': 'application/json',
        'x-redlock-auth': auth_jwt
    }

    response = requests.request("PUT", api_url, headers=headers, data=payload)

    print("DELETE ACCOUNT GROUP " + account_group + "\n")

    payload={}
    headers = {
        'x-redlock-auth': auth_jwt
    }

    response = requests.request("DELETE", api_url, headers=headers, data=payload)