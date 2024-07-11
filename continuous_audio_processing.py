import requests
import time

def test_audio_prediction(audio_file_path, url):
    """
    Sends an audio file to the microservice and prints the response.

    Parameters:
        audio_file_path (str): The path to the audio file.
        url (str): The URL of the microservice endpoint.
    """
    # Open the audio file in binary mode
    with open(audio_file_path, 'rb') as file:
        files = {'file': (audio_file_path, file, 'audio/ogg')}
        response = requests.post(url, files=files)

    return response

if __name__ == '__main__':
    # URL of the microservice
    # Ensure the IP address and port match the Docker container's exposed settings
    service_url = 'http://10.0.1.60:5000/predict'
    test_audio_path = '/home/koala/Desktop/soundscape_29201.ogg'
    total_time = 0

    for i in range(12):
        start_time = time.time()  
        response = test_audio_prediction(test_audio_path, service_url)
        end_time = time.time() 
        time_taken = end_time - start_time
        print(f"Request {i+1}: Time taken = {time_taken:.2f} seconds")

        if response.status_code == 200:
            print("Prediction received successfully!")
            print(response.json())
        else:
            print("Failed to get prediction.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    print(f"Total time taken for 12 requests: {total_time:.2f} seconds")