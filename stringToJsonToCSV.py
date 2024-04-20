import json
import re
import pandas as pd
import os

def extract_and_convert_to_csv(agencyName, incomingData, output_file):
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
    json_match = re.search(r'{.*?}', incomingData, re.DOTALL)
    if json_match:
        json_string = json_match.group(0)

        # Parse the JSON string
        data = json.loads(json_string)

        # Flatten the nested JSON structure
        flattened_data = flatten_dict(data)

        # Convert flattened data to DataFrame
        df = pd.DataFrame([flattened_data])

        # Add additional string as the first column
        df.insert(0, 'Agency_Name', agencyName)

        # Append DataFrame to CSV file
        if os.path.exists(output_file):
            df.to_csv(output_file, mode='a', index=False, header=False)
        else:
            df.to_csv(output_file, index=False)

    else:
        print("No JSON data found in the string.")

# Example usage:
agencyName = "ARMY"
incomingData = '''
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
output_file = "output.csv"

# Call the function multiple times
extract_and_convert_to_csv(agencyName, incomingData, output_file)
# Call it again with another incomingData if needed
# extract_and_convert_to_csv(another_agencyName, another_incomingData, output_file)
extract_and_convert_to_csv(agencyName, incomingData, output_file)
extract_and_convert_to_csv(agencyName, incomingData, output_file)
