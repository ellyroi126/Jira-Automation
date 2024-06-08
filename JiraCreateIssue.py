import requests
import argparse
import json

#Get API_KEY 
def get_api_token(url):
  token_url = requests.get(url)

  return token_url.text.strip('"').strip('"')

def create_jira_issue(base_url, headers, summary):
  jira_url = f"{base_url}/rest/api/3/issue/"

  issue_body = {
    "fields": {
      "project": {
        "key": "GISIMT"
      },
      "issuetype": {  
        "name": "Incident Request"
      },
      "summary": summary,
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": "This is a test description"
              }
            ]
          }
        ]
      }
    }
  }

  response = requests.post(jira_url, headers=headers, json=issue_body)

  if response.status_code == 201:
      print("Issue created successfully!")
  else:
      print("Failed to add comment:", response.status_code)

def main():
  parser = argparse.ArgumentParser(description='Create a Jira issue with a custom summary.')
  parser.add_argument('status', type=str, help='Status to include in the issue summary (e.g., RESOLVED, PROBLEM)')
  args = parser.parse_args()

  url = "https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265"
  base_url = "https://api.atlassian.com/ex/jira/440a7ad1-478f-4a05-9f98-bc29f46b75b5"
  token = get_api_token(url)

  headers = {
      "Authorization":f"Bearer {token}",
      "Content-Type":"application/json"
  }

  summary = f"[DO NOT DELETE - ERDF TEST ISSUE] [{args.status}]"

  create_jira_issue(base_url, headers, summary)

if __name__ == "__main__":
    main()