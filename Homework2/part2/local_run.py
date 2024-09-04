import requests
import json

url = 'http://localhost:11434/api/generate'

payload = {
    "model": "llama3.1",
    "prompt": "What color is the sky at different times of the day?",
    # "format": "json",
    "stream": False
}

# Send the request
response = requests.post(url, json=payload)

# Print the response
print(response.json()['response'])