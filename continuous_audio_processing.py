        import os
        import time
        import requests
        from datetime import datetime
        import json
        from collections import defaultdict

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
            start_time = time.time()
            
            # Open the audio file in binary mode
            with open(audio_file_path, 'rb') as file:
                files = {'file': (os.path.basename(audio_file_path), file, 'audio/ogg')}
                response = requests.post(url, files=files)

            end_time = time.time()
            duration = end_time - start_time

            if response.status_code == 200:
                print(f"Prediction received successfully! Time taken: {duration:.2f} seconds")
                result = response.json()
                print(result)
                
                date_output_folder = os.path.join(output_folder, pi_id, date)
                os.makedirs(date_output_folder, exist_ok=True)

                # Save result as JSON with audio file name
                audio_file_name = os.path.splitext(os.path.basename(audio_file_path))[0]
                individual_output_file_path = os.path.join(date_output_folder, f'{audio_file_name}.json')
                
                # Load existing data if the file already exists
                if os.path.exists(individual_output_file_path):
                    with open(individual_output_file_path, 'r') as infile:
                        existing_data = json.load(infile)
                else:
                    existing_data = {"pi_id": pi_id, "date": date, "species": []}
                
                # Append the new result
                existing_data["species"].append(result)
                
                # Save individual result
                with open(individual_output_file_path, 'w') as outfile:
                    json.dump(existing_data, outfile)
                    print(f"Saved individual result JSON successfully: {individual_output_file_path}")

                # Combine results into date.json
                date_json_file_path = os.path.join(date_output_folder, f'{date}.json')
                if os.path.exists(date_json_file_path):
                    with open(date_json_file_path, 'r') as infile:
                        combined_data = json.load(infile)
                else:
                    combined_data = {"pi_id": pi_id, "date": date, "results": {}}
                
                combined_data["results"][audio_file_name] = result
                
                with open(date_json_file_path, 'w') as outfile:
                    json.dump(combined_data, outfile)
                    print(f"Saved combined result JSON successfully: {date_json_file_path}")
                
            else:
                print(f"Failed to get prediction. Time taken: {duration:.2f} seconds")
                print("Status Code:", response.status_code)
                print("Response:", response.text)

        def process_all_sites(base_folder, service_url, output_folder):
            start_time = time.time()

            pi_dirs = [d for d in os.listdir(base_folder) if d.startswith('RPiID-')]
            site_files = defaultdict(list)

            # Collect all files in order
            for pi_dir in pi_dirs:
                pi_path = os.path.join(base_folder, pi_dir)
                for date_dir in os.listdir(pi_path):
                    date_path = os.path.join(pi_path, date_dir)
                    for file in os.listdir(date_path):
                        if file.endswith('.wav'):
                            site_files[pi_dir].append((os.path.join(date_path, file), date_dir))
            
            # Sort files by date and filename before sending
            for pi_id in site_files:
                site_files[pi_id].sort(key=lambda x: (x[1], x[0]))

            # Process files alternately from each site
            while any(site_files.values()):
                for pi_id in pi_dirs:
                    if site_files[pi_id]:
                        audio_file, date = site_files[pi_id].pop(0)
                        print(f"Processing file from {pi_id} on {date}: {os.path.basename(audio_file)}")
                        test_audio_prediction(audio_file, service_url, output_folder, pi_id, date)
            
            end_time = time.time()
            total_duration = end_time - start_time
            print(f"Total time taken for processing all files: {total_duration:.2f} seconds")

        if __name__ == '__main__':
            service_url = 'http://10.0.1.60:5000/predict'
            base_folder = '/home/kaung-ftp/ftp/continuous_monitoring_data/live_data/'
            output_folder = '/home/koala/Desktop/results/'
            
            process_all_sites(base_folder, service_url, output_folder)
