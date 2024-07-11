import os
import time
import requests
from datetime import datetime, timedelta
import json

def test_audio_prediction(audio_file_path, url, output_folder, pi_id, date):
    """
    Sends an audio file to the microservice, prints the response, and saves it as a JSON file.

    Parameters:
        audio_file_path (str): The path to the audio file.
        url (str): The URL of the microservice endpoint.
        output_folder (str): The folder to save the JSON results.
        pi_id (str): Identifier for the Raspberry Pi.
        date (str): Date of the audio file.
    """
    # Open the audio file in binary mode
    with open(audio_file_path, 'rb') as file:
        files = {'file': (os.path.basename(audio_file_path), file, 'audio/ogg')}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("Prediction received successfully!")
        result = response.json()
        print(result)
        # Save result as JSON
        output_file_name = f"{pi_id}_{date}.json"
        output_file_path = os.path.join(output_folder, output_file_name)
        with open(output_file_path, 'w') as outfile:
            json.dump({"pi_id": pi_id, "date": date, "results": result}, outfile)
            print("Saved results json successfully")
    else:
        print("Failed to get prediction.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)

def process_all_sites(base_folder, service_url, output_folder):
    pi_dirs = [d for d in os.listdir(base_folder) if d.startswith('RPiID-')]
    all_files = []

    # Collect all files first to process them in order
    for pi_dir in pi_dirs:
        pi_path = os.path.join(base_folder, pi_dir)
        for date_dir in os.listdir(pi_path):
            date_path = os.path.join(pi_path, date_dir)
            for file in os.listdir(date_path):
                if file.endswith('.wav'):
                    all_files.append((os.path.join(date_path, file), pi_dir, date_dir))

    # Sort files by date and filename before sending
    all_files.sort(key=lambda x: (x[2], x[0]))

    for audio_file, pi_id, date in all_files:
        print(f"Processing file from {pi_id} on {date}: {os.path.basename(audio_file)}")
        test_audio_prediction(audio_file, service_url, output_folder, pi_id, date)

if __name__ == '__main__':
    service_url = 'http://10.0.1.60:5000/predict'
    base_folder = '/home/kaung-ftp/ftp/continuous_monitoring_data/live_data/'
    output_folder = '/home/koala/Desktop/results/'
    
    process_all_sites(base_folder, service_url, output_folder)
