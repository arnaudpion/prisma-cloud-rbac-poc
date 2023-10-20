#!/usr/bin/env python3

import os
import requests
import json


### Credentials for API Authentication ###
username = os.environ.get('PC_PY_IDENTITY')  # Access Key in Prisma Cloud
password = os.environ.get('PC_PY_SECRET')    # Secret Key in Prisma Cloud


### API Endpoint ###
url = os.environ.get('PC_PY_URL')  # Prisma Cloud API URL - Check https://pan.dev/prisma-cloud/api/cspm/api-urls/


### Other Variables ###
account_prefix = "test"  # Allows to apply the logic to a subset of existing accounts in Prisma Cloud for testing purpose
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


### Retrieve Accounts List ###
payload={}
headers = {
  'Accept': 'application/json; charset=UTF-8',
  'x-redlock-auth': auth_jwt
}

response = requests.request("GET", url+"/cloud", headers=headers, data=payload)
json_response = json.loads(response.content)


### Add RQL Request that Checks Tags Assigned to an Account ###


### List All Accounts that Start with account_prefix ###
print("\n\n+++ LISTING ACCOUNTS +++\n")
for account in json_response:
    if account['name'].startswith(account_prefix):
        print(account['name'])
        print(account['accountId']+ "\n")
        account_list.append(account['accountId'])


### Create an Account Group for Each Account that Starts with account_prefix (Accounts Listed in account_list Variable) ###
print("\n\n+++ CREATING ACCOUNT GROUPS +++\n")

for account in account_list:
    payload = json.dumps({
        "accountIds": [account],
        "description": "TEST - Account Group for Account ID " + account,
        "name": account_prefix + " - TEST GROUP - " + account
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': auth_jwt
    }

    response = requests.request("POST", url+'/cloud/group', headers=headers, data=payload)
    print(response.text + "\n")
    json_response = json.loads(response.content)
    account_group_list.append(json_response['id'])


### Create a Role for Each Account Group Created ###
print("\n\n+++ CREATING ROLES +++\n")

for account_group in account_group_list:

    payload = json.dumps({
        "accountGroupIds": [
            account_group
        ],
        "description": "TEST - Account Group Admin Role for Account ID " + account_group,
        "name": account_prefix + " - TEST ROLE - " + account_group,
        "roleType": "Account Group Admin"
    })

    headers = {
        'Content-Type': 'application/json',
        'x-redlock-auth': auth_jwt
    }

    response = requests.request("POST", url + "/user/role", headers=headers, data=payload)
    print(response.text + "\n")
    json_response = json.loads(response.content)
    role_list.append(json_response['id'])


### Script Output for Future Deletion / Clean Up of Created Items ###
print("\n\n+++ OUTPUT FOR CLEAN UP +++\n")
print("account_prefix = \"" + account_prefix + "\"")
print("account_list =", account_list)
print("account_group_list =", account_group_list)
print("role_list =", role_list)