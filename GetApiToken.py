import requests

#Get API_KEY 
token_url = requests.get("https://y6u7rbcg9g.execute-api.us-west-2.amazonaws.com/prod/sandbox265")

token = token_url.text.strip('"').strip('"')

print(token)

