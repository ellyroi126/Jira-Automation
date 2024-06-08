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

issue_key = "GISIMT-11836"
jira_url = f"{base_url}/rest/api/3/issue/{issue_key}/comment"

comment_body = {
 "body" : {
    "content": [
      {
        "content": [
          {
            "text" : """Problem has been resolved in 13m 0s at 15:51:05 on 2024.05.31
            Problem name: High memory utilization ( >90% for 15m)
            Host: sjc1-te-ftp02.sdi.trendnet.org
            Severity: Warning
            Original problem ID: 124177203""",

            "type": "text"
          }
        ],
        "type": "paragraph"
      }
    ],
    "type": "doc",
    "version": 1
  }
}

response = requests.post(jira_url, headers=headers, json=comment_body)

if response.status_code == 201:
    print("Comment added successfully!")
else:
    print("Failed to add comment:", response.status_code)




'''

"text": """OMEGA_PWP_EKS_P0_RegisterSeat.py-s247-an1 is Up 

            Integration Name-JiraCloud Prod
            ----------------------------------------
            Display Name : OMEGA_PWP_EKS_P0_RegisterSeat.py-s247-an1 

            Monitor Groups : PWP 

            Tags:webhook

            Monitor Type : PLUGIN 

            Monitor status : Up 

            Available since : June 1, 2024, 1:51 PM CST 

            Reason :  

            Dashboard link : https://www.site24x7.com/app/client#/home/monitors/392874000037780008/Summary """

'''

'''

"text" : """Problem has been resolved in 13m 0s at 15:51:05 on 2024.05.31
            Problem name: High memory utilization ( >90% for 15m)
            Host: sjc1-te-ftp02.sdi.trendnet.org
            Severity: Warning
            Original problem ID: 124177203"""

'''