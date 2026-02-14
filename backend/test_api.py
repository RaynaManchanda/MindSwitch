import requests

url = "http://127.0.0.1:5000/generate_hint"

data = {
    "mode": "DSA"
}

response = requests.post(url, json=data)

print(response.json())
