import json
import re
import csv

def extract_and_convert_to_csv(mixed_string, output_file):
    # Function to flatten nested dictionaries
    def flatten_dict(d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    # Use regular expressions to extract JSON portion
    json_match = re.search(r'{.*?}', mixed_string, re.DOTALL)
    if json_match:
        json_string = json_match.group(0)

        # Parse the JSON string
        data = json.loads(json_string)

        # Flatten the nested JSON structure
        flattened_data = flatten_dict(data)

        # Write flattened data to CSV in append mode
        with open(output_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=flattened_data.keys())
            # Check if the file is empty; if so, write header
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(flattened_data)
    else:
        print("No JSON data found in the string.")

# Example usage:
mixed_string = '''
{
    "contractor": "Lockheed Martin Rotary and Mission Systems",
    "location": "Owego, New York",
    "cost": "$88,380,255",
    "purpose": "overhaul of B-2 digital receiver and legacy defense message system",
    "completion_date": "April 16, 2034",
    "work_location": "Owego, New York",
    "contract_number": "FA8119-24-D-0008",
    "contracting_activity": "Air Force Sustainment Center, Tinker Air Force Base, Oklahoma"
}
'''
output_file = "outpu1t.csv"

# Call the function multiple times
extract_and_convert_to_csv(mixed_string, output_file)
# Call it again with another mixed_string if needed
# extract_and_convert_to_csv(another_mixed_string, output_file)
extract_and_convert_to_csv(mixed_string, output_file)
extract_and_convert_to_csv(mixed_string, output_file)