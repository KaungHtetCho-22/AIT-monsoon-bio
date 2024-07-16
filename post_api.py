import requests
import json

access_token = 'XXXX' # add access_token

sensor_data = 'output.json'

with open(sensor_data, 'r') as file:
    sensor_data = json.load(file)

url = 'https://apple.com/apple/API/SendIoTDevice' # change URL

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
}

# Convert sensor data to JSON string
sensor_data_json = json.dumps(sensor_data)

# Send POST request with sensor data
response = requests.post(url, headers=headers, data=sensor_data_json)

# Check response
if response.status_code == 200:
    print('Sensor data sent successfully.')
    try:
        response_json = response.json()
        print('Parsed JSON response:')
        print(json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print('Response is not in JSON format')
else:
    print(f'Failed to send sensor data. Status code: {response.status_code}')
    print('Response content:')
    print(response.text)

print('\nResponse Details:')
print(f'Status Code: {response.status_code}')


