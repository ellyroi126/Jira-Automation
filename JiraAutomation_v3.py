import requests
from datetime import datetime, timezone, timedelta
import pytz

def get_api_token(token_url):
    response = requests.get(token_url)
    
    return response.text.strip('"').strip('"')

def get_time_elapsed(issue_details):
    created_time_str = issue_details['fields']['created']
    created_time = datetime.strptime(created_time_str, '%Y-%m-%dT%H:%M:%S.%f%z')
    ph_tz = pytz.timezone('Asia/Manila')
    current_time = datetime.now(ph_tz)
    time_elapsed = current_time - created_time
    return time_elapsed

def get_comments(base_url, headers, issue_key):
    jira_url = f"{base_url}/rest/api/3/issue/{issue_key}/comment"

    response = requests.get(jira_url, headers=headers)
    return response.json()['comments']

def get_issues(base_url, headers, jql):
    jira_url = f'{base_url}/rest/api/3/search'
    params = {
        'jql': jql,
        'startAt': 0,
        'maxResults': 100,
        'fields': 'project,summary,status,issuetype,assignee,reporter,priority,created'
    }
    response = requests.get(jira_url, headers=headers, params=params)
    
    return response.json().get('issues', [])

def transition_issue(base_url, headers, issue_key, transition_id):
    transition_url = f'{base_url}/rest/api/3/issue/{issue_key}/transitions'
    payload = {
        "transition": {
            "id" : transition_id
        }
    }
    response = requests.post(transition_url, headers=headers, json=payload)

def change_assignee(base_url, header_assignee, issue_key):
    assignee_url = f"{base_url}/rest/api/3/issue/{issue_key}/assignee"
    assignee_data = {
        "accountId": "63bf4bf90a1b5442166ad8fb"
    }
    
    response = requests.put(assignee_url, headers=header_assignee, json=assignee_data)

def add_comment(base_url, headers, issue_key, comment_body):
    comment_url = f'{base_url}/rest/api/3/issue/{issue_key}/comment'
    payload = {
        "body": {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": comment_body,
                            "type": "text"
                        }
                    ]
                }
            ]
        }
    }
    response = requests.post(comment_url, headers=headers, json=payload)

def new_issues(base_url, headers, jql_new):
    try:

        issues = get_issues(base_url, headers, jql_new)

        for issue in issues:
            summary = issue['fields']['summary']
            issue_key = issue['key']
            time_elapsed = get_time_elapsed(issue)
            comments = get_comments(base_url, headers, issue_key)
            comment_body = f"""This issue has resolved on its own and has been automatically transitioned to 'VOID'.

Time Elapsed : {str(time_elapsed).split('.')[0]}"""

            has_resolved_or_up = any("resolved" in comment['body']['content'][0]['content'][0]['text'] or 
                                     "Up" in comment['body']['content'][0]['content'][0]['text'] 
                                     for comment in comments)

            if has_resolved_or_up:
                print(f"Processing issue {issue_key} with summary '{summary}'")

                #Auto_assign to isserviceops@trendmicro.com
                change_assignee(base_url, headers, issue_key)
                #print(f"Issue {issue_key} assigned to isserviceops@trendmicro.com")
                
                #Transitions
                transition_issue(base_url, headers, issue_key, "91")
                transition_issue(base_url, headers, issue_key, "11")
                transition_issue(base_url, headers, issue_key, "101")
                
                #Add Comment after transitioning
                add_comment(base_url, headers, issue_key, comment_body)

            else:
                change_assignee(base_url, headers, issue_key)

                transition_issue(base_url, headers, issue_key, "91")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def inProgress_issues(base_url, headers, jql_inProgress):
    automated_accountId = "63bf4bf90a1b5442166ad8fb"
    try:

        issues = get_issues(base_url, headers, jql_inProgress)
        #print(f"Retrieved {len(issues)} issues")

        for issue in issues:
            summary = issue['fields']['summary']
            issue_key = issue['key']
            time_elapsed = get_time_elapsed(issue)
            comments = get_comments(base_url, headers, issue_key)
            comment_body = f"""This issue has resolved on its own and has been automatically transitioned to 'VOID'.

Time Elapsed : {str(time_elapsed).split('.')[0]}"""
            #print(f"Issue {issue_key} has {len(comments)} comments")

            has_foreign_comment = any(comment['author']['accountId'] != automated_accountId for comment in comments)
            has_resolved_or_up = any("resolved" in comment['body']['content'][0]['content'][0]['text'] or 
                                     "Up" in comment['body']['content'][0]['content'][0]['text'] 
                                     for comment in comments)
            
            if has_resolved_or_up:
                #Check if there are no other comments except for the automation
                if not comments or not has_foreign_comment:
                    #print(f"Processing issue {issue_key} with summary '{summary}'")
                    
                    #Transitions
                    transition_issue(base_url, headers, issue_key, "11")
                    transition_issue(base_url, headers, issue_key, "101")
                    
                    #Add Comment after transitioning
                    add_comment(base_url, headers, issue_key, comment_body)

                else:
                    transition_issue(base_url, headers, issue_key, "11")
                    transition_issue(base_url, headers, issue_key, "31")

            else:
                if has_foreign_comment:
                    transition_issue(base_url, headers, issue_key, "11")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def verification_issues(base_url, headers, jql_verification):
    automated_accountId = "63bf4bf90a1b5442166ad8fb"
    try:

        issues = get_issues(base_url, headers, jql_verification)
        #print(f"Retrieved {len(issues)} issues")

        for issue in issues:
            issue_key = issue['key']
            comments = get_comments(base_url, headers, issue_key)
            #print(f"Issue {issue_key} has {len(comments)} comments")

            has_foreign_comment = any(comment['author']['accountId'] != automated_accountId for comment in comments)
            has_resolved_or_up = any("resolved" in comment['body']['content'][0]['content'][0]['text'] or 
                                     "Up" in comment['body']['content'][0]['content'][0]['text'] 
                                     for comment in comments)

            if has_resolved_or_up:
                if comments or has_foreign_comment:
                #Transitions
                    transition_issue(base_url, headers, issue_key, "31")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def filter_issue_priority(base_url, headers, jql_new, jql_inProgress, jql_verification):
    try:
        issues_new = get_issues(base_url, headers, jql_new)
        issues_inProg = get_issues(base_url, headers, jql_inProgress)
        issues_verif = get_issues(base_url, headers, jql_verification)
        

        all_issues = issues_new + issues_inProg + issues_verif
        priority_response_times = {
            "P0": timedelta(minutes=15),
            "P1": timedelta(minutes=30),
            "P2": timedelta(hours=1),
            "P3": timedelta(hours=2)
        }

        for issue in all_issues:
            priority_name = issue['fields']['priority']['name']
            issue_key = issue['key']
            time_elapsed = get_time_elapsed(issue)
            comments = get_comments(base_url, headers, issue_key)
            print(f"Time Elapsed for {issue_key} =='{time_elapsed}'")

            has_resolved_or_up = any("resolved" in comment['body']['content'][0]['content'][0]['text'] or 
                                     "Up" in comment['body']['content'][0]['content'][0]['text'] 
                                     for comment in comments)

            if not has_resolved_or_up:
                if priority_name in priority_response_times and time_elapsed > priority_response_times[priority_name]:
                    comment_body = f"""This issue has exceeded the response time.

Priority : {priority_name}

Target response time: {priority_response_times[priority_name]}

Time Elapsed : {str(time_elapsed).split('.')[0]}"""

                    add_comment(base_url, headers, issue_key, comment_body)
                    print("Added comment for this priority")

    except Exception as e:
        print(f"An error occurred: {e}")

def main():

    #Get API_KEY 
    token_url = "https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265"
    token=get_api_token(token_url)
    base_url = "https://api.atlassian.com/ex/jira/440a7ad1-478f-4a05-9f98-bc29f46b75b5"

    jql_new = "project = GISIMT AND status = 'NEW'"
    jql_inProgress = "project = GISIMT AND status = 'Request for Authentication'"
    jql_verification = "project = GISIMT AND status = 'Verification'"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    header_assigne = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    new_issues(base_url, headers, jql_new)
    inProgress_issues(base_url, headers, jql_inProgress)
    verification_issues(base_url, headers, jql_verification)
    filter_issue_priority(base_url, headers, jql_new, jql_inProgress, jql_verification)

if __name__ == "__main__":
    main()