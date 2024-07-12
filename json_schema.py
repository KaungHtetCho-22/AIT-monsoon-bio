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
    output = defaultdict(lambda: defaultdict(list))
    
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
                
                # Combine species hourly counts under the same date for each pi_id
                for species, counts in hourly_counts.items():
                    if not output[pi_id][date]:
                        output[pi_id][date] = {species: counts}
                    else:
                        if species in output[pi_id][date]:
                            output[pi_id][date][species] = [
                                output[pi_id][date][species][i] + counts[i] for i in range(24)
                            ]
                        else:
                            output[pi_id][date][species] = counts
    
    # Convert defaultdict to regular dict before returning
    return {pi_id: dict(dates) for pi_id, dates in output.items()}

input_dir = 'sample_json'

output_json = create_output_json(input_dir)

with open('output.json', 'w') as outfile:
    json.dump(output_json, outfile, indent=2)

print("Output JSON has been written to 'output.json'")
