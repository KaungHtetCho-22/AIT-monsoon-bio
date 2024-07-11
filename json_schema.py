import os
import json
from collections import defaultdict

def combine_json_results(output_folder):
    """
    Combines all existing date.json files into a consolidated JSON structure.

    Parameters:
        output_folder (str): The folder where individual date folders are located.
    """
    combined_results = defaultdict(list)

    # Iterate through each pi_id folder
    for pi_id in os.listdir(output_folder):
        pi_path = os.path.join(output_folder, pi_id)
        if os.path.isdir(pi_path):
            # Iterate through each date folder for the pi_id
            for date in os.listdir(pi_path):
                date_path = os.path.join(pi_path, date)
                if os.path.isdir(date_path):
                    date_json_file = os.path.join(date_path, f"{date}.json")
                    if os.path.exists(date_json_file):
                        with open(date_json_file, 'r') as infile:
                            date_data = json.load(infile)
                            combined_results[pi_id].append(date_data)

    # Save combined results
    combined_output_file = os.path.join(output_folder, f'{date}.json')
    with open(combined_output_file, 'w') as outfile:
        json.dump(combined_results, outfile, indent=4)
        print(f"Combined results saved successfully: {combined_output_file}")

if __name__ == '__main__':
    output_folder = '/home/koala/Desktop/results/'
    
    combine_json_results(output_folder)
