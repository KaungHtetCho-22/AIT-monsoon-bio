import os
import json

def combine_json_results(folder_path, target_date):
    """
    Combine JSON files by date and save the combined results in a single JSON file.

    Parameters:
        folder_path (str): The path to the folder containing the JSON files.
        target_date (str): The target date in the filename to filter and combine the results.
    """
    combined_results = {"date": target_date, "results": []}
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.json') and target_date in filename:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                combined_results["results"].append(data)

    # Save the combined results to a new JSON file
    output_file_path = os.path.join(folder_path, f"combined_{target_date}.json")
    with open(output_file_path, 'w') as outfile:
        json.dump(combined_results, outfile)
    
    print(f"Combined results saved to {output_file_path}")

if __name__ == '__main__':
    folder_path = '/home/koala/Desktop/results/'  
    target_date = "12-02-49"  
    
    combine_json_results(folder_path, target_date)