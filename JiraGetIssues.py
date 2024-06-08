import requests
from urllib.parse import urlparse, parse_qs
from requests.auth import HTTPBasicAuth
import json

#Get API_KEY 
token_url = requests.get("https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265")

base_url = "https://api.atlassian.com/ex/jira/440a7ad1-478f-4a05-9f98-bc29f46b75b5"
token = token_url.text.strip('"').strip('"')
jql = "status = 'NEW'"

headers = {
    "Authorization":f"Bearer {token}",
    "Content-Type":"application/json"
}

params = {
    'jql': jql,
    'startAt': 0,
    'maxResults': 100,
    'fields': 'project,summary,status,issuetype,assignee,reporter'
}

jira_url = f"{base_url}/rest/api/3/search"

response = requests.get(jira_url, headers=headers, params=params)

issues = response.json().get('issues', [])

if issues:
        print(f"Found {len(issues)} issues:")
        for issue in issues:
            project = issue['fields']['project']['key']
            summary = issue['fields']['summary']
            status = issue['fields']['status']['name']
            issuetype = issue['fields']['issuetype']['name']
            assignee = issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else "Unassigned"
            reporter = issue['fields']['reporter']['displayName'] if issue['fields']['reporter'] else "No reporter"
            print(f"Project: {project}, Key: {issue['key']}, Summary: {summary}, "
                  f"Status: {status}, Issue Type: {issuetype}, "
                  f"Assignee: {assignee}, Reporter: {reporter}")
else:
    print("No issues found.")



