import requests
import json

url = "http://127.0.0.1:8000"
data = {"name": "Bernard", "Coding ability": "Excellent"}

response_json = requests.post(url, json=json.dumps(data))
print("Status json: ", response_json.status_code)
print("Response json: ", response_json.text)
print("Response text: ", response_json.json())