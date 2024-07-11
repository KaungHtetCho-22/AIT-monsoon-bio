import requests
import time
import os

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

def get_audio_files_from_folders(folder_paths):
    """
    Retrieves all audio files from the given list of folders.

    Parameters:
        folder_paths (list): A list of folder paths.

    Returns:
        list: A list of tuples containing (folder_path, audio_file_path).
    """
    audio_files = []
    for folder in folder_paths:
        for file_name in os.listdir(folder):
            if file_name.endswith('.ogg'):
                audio_files.append((folder, os.path.join(folder, file_name)))
    return audio_files

if __name__ == '__main__':
    # URL of the microservice
    service_url = 'http://10.0.1.60:5000/predict'
    # Paths to the 12 folders
    folder_paths = [
        '/path/to/folder1', '/path/to/folder2', '/path/to/folder3', '/path/to/folder4',
        '/path/to/folder5', '/path/to/folder6', '/path/to/folder7', '/path/to/folder8',
        '/path/to/folder9', '/path/to/folder10', '/path/to/folder11', '/path/to/folder12'
    ]

    # Get all audio files from the folders
    audio_files = get_audio_files_from_folders(folder_paths)
    total_time = 0

    # Send each audio file to the server in a round-robin manner
    for i, (folder, audio_file_path) in enumerate(audio_files):
        start_time = time.time()
        response = test_audio_prediction(audio_file_path, service_url)
        end_time = time.time()
        time_taken = end_time - start_time
        total_time += time_taken

        print(f"Request {i+1} from folder {folder}: Time taken = {time_taken:.2f} seconds")

        if response.status_code == 200:
            print("Prediction received successfully!")
            print(response.json())
        else:
            print("Failed to get prediction.")
            print("Status Code:", response.status_code)
            print("Response:", response.text)

    print(f"Total time taken for {len(audio_files)} requests: {total_time:.2f} seconds")
