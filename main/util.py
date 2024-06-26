import re
import pandas as pd
import os
import json

def extract_and_convert_to_csv(additional_string, mixed_string, output_file):
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
        try:
            data = json.loads(json_string)

            # Flatten the nested JSON structure
            flattened_data = flatten_dict(data)

            # Convert flattened data to DataFrame
            df = pd.DataFrame([flattened_data])

            # Add additional string as the first column
            df.insert(0, 'agency_name', additional_string)

            # Append DataFrame to CSV file
            if os.path.exists(output_file):
                df.to_csv(output_file, mode='a', index=False, header=False)
            else:
                df.to_csv(output_file, index=False)
        except:
            print("Failed to parse JSON data.")

    else:
        print("No JSON data found in the string.")


def clean_data(data):
    left = 0
    right =-1
    while left<len(data) and data[left] != '{':
        left+=1
    while right>-len(data) and data[right] != '}':
        right-=1
    return data[left:right+1]
