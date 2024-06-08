import requests
from urllib.parse import urlparse, parse_qs
from requests.auth import HTTPBasicAuth
import json

#Get API_KEY 
token_url = requests.get("https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265")

base_url = "https://api.atlassian.com/ex/jira/440a7ad1-478f-4a05-9f98-bc29f46b75b5"
token = token_url.text.strip('"').strip('"')

headers = {
    "Authorization":f"Bearer {token}",
    "Content-Type":"application/json",
    "Accept":"application/json"
}

issue_key = "GISIMT-11524"
jira_url = f"{base_url}/rest/api/3/issue/{issue_key}/transitions"

"""
Transition IDs:
    "id": "91" - In Progress
    "id": "11" - Verification
    "id": "101" - Void
    "id": "31" - Closed
"""

transition_body = {
 "transition": {
    "id": "91"
  }
}

response = requests.post(jira_url, headers=headers, json=transition_body)

if response.status_code == 201:
    print("Issue transitioned successfully!")
else:
    print("Failed to add comment:", response.status_code)