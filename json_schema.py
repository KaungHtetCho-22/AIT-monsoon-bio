import json
from collections import defaultdict
import os

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def count_hourly_occurrences(species_data):
    hourly_counts = defaultdict(lambda: [0] * 24)
    for entry in species_data:
        for time_stamp, data in entry.items():
            # Extract the hour from the time_stamp
            hour_str = time_stamp.split('_')[0]
            hour = int(hour_str.split('-')[0])
            species = data['Class']
            hourly_counts[species][hour] += 1
    return dict(hourly_counts)

def create_output_json(input_dir):
    output = defaultdict(list)
    
    # Traverse through the directory and find all JSON files
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                data = process_json_file(file_path)
                pi_id = data['pi_id']
                date = data['date']
                species_data = data['species']
                
                hourly_counts = count_hourly_occurrences(species_data)
                
                # Prepare the entry with mock coordinates and scores
                entry = {
                    "date": date,
                    "coordinate": [18.8018, 98.9948],  # Mock coordinates
                    "score": 5,  # Mock score
                    "species": hourly_counts
                }
                
                # Check if the entry for the date already exists
                existing_entry = next((item for item in output[pi_id] if item["date"] == date), None)
                if existing_entry:
                    for species, counts in hourly_counts.items():
                        if species in existing_entry["species"]:
                            existing_entry["species"][species] = [
                                existing_entry["species"][species][i] + counts[i] for i in range(24)
                            ]
                        else:
                            existing_entry["species"][species] = counts
                else:
                    output[pi_id].append(entry)
    
    # Convert defaultdict to regular dict before returning
    return dict(output)

# Directory containing JSON files
input_dir = 'sample_json'

# Generate the output JSON
output_json = create_output_json(input_dir)

# Write the output to a file
with open('output.json', 'w') as outfile:
    json.dump(output_json, outfile, indent=2)

print("Output JSON has been written to 'output.json'")
