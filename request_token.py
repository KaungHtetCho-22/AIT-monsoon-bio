import requests

url = "https://apple.com/apple/API/SendIoTDevice"
data = {
    "grant_type": "password",
    "client_id": "id",
    "client_secret": "secret",
    "username": "username",
    "password": "passwd",
    "scope": "scope"
}

response = requests.post(url, data=data)

try:
    response.raise_for_status()  # Check for HTTP request errors
    json_response = response.json()  
    print(json_response)
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")  # HTTP error (e.g., 404, 500, etc.)
    print(response.text)  
except requests.exceptions.RequestException as req_err:
    print(f"Request error occurred: {req_err}")  # General request error
    print(response.text)  
except ValueError as json_err:
    print(f"JSON decode error: {json_err}")  # JSON parsing error
    print(response.text)  