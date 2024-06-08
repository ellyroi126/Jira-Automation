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
    "Content-Type":"application/json"
}

issue_key = "GISIMT-11801"
jira_url = f"{base_url}/rest/api/3/issue/{issue_key}"

response = requests.request(
    "DELETE",
    jira_url,
    headers=headers,
    params={
        'deleteSubtasks': 'true',
    }
)

if response.status_code == 204:
    print("Issue deleted successfully!")
else:
    print("Failed to delete issue:", response.status_code)