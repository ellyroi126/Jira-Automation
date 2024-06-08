import requests
import json

def get_api_token(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip('"').strip('"')
    else:
        raise Exception("Failed to get API token")

def get_account_id(base_url, headers, query):
    search_url = f"{base_url}/rest/api/3/user/search"
    params = {
        'query': query
    }
    
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0]['accountId']
        else:
            raise Exception(f"No user found with query: {query}")
    else:
        raise Exception(f"Failed to search for user: {response.status_code} {response.text}")

def main():
    # URL to get the API token
    token_url = "https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265"
    
    # Base URL for Jira API
    base_url = "https://api.atlassian.com/ex/jira/440a7ad1-478f-4a05-9f98-bc29f46b75b5"
    
    token = get_api_token(token_url)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    query = "isserviceops@trendmicro.com"  
    
    try:
        account_id = get_account_id(base_url, headers, query)
        print(f"Account ID for {query}: {account_id}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()