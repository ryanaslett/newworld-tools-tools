import sys
import json
import yaml
from pathlib import Path

def process_item_keys(obj, table_name, item_keys, yaml_data, key_type):
    for item_key in item_keys:
        if obj[item_key] and obj[item_key].strip():
            if item_key not in yaml_data[table_name]:
                yaml_data[table_name][item_key] = {}
            yaml_data[table_name][item_key].update({key_type: obj[item_key]})

def main():
    # Check that a filename was provided
    if len(sys.argv) < 2:
        print("Please provide the filename of the input JSON file as a command-line argument.")
        sys.exit()

    # Load the JSON data from the specified file
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        data = json.load(f)  # Load JSON directly from the file

    # Create a dictionary for the output YAML data
    yaml_data = {}

    # Loop through each JSON object and populate the YAML data dictionary
    for obj in data:
        table_name = obj['LootTableID']
        if table_name.endswith('_Probs'):
            table_name = table_name.replace('_Probs', '')
            key_type = 'Threshold'
            if yaml_data.get(table_name) is not None:
                yaml_data[table_name]['MaxRoll'] = obj['MaxRoll']
        elif table_name.endswith('_Qty'):
            table_name = table_name.replace('_Qty', '')
            key_type = 'Qty'
        else:
            # We have a new loot Table.
            yaml_data[table_name] = {}
            # Define a list of field names to assign to the YAML data
            loot_table_metadata = ['RollBonusSetting', 'AND/OR', 'Conditions', 'ConditionOverridesRoll', 'TriggerLimitOnVisit', 'UseLevelGS', 'HWMMult',
                           'ChanceToExceedIndex', 'GSBonus']

            # Loop over the field names and optionally set the value in the YAML data
            for field_name in loot_table_metadata:
                value = obj.get(field_name, None)
                if value and str(value).strip():
                    yaml_data[table_name][field_name] = value
            # Find all Item keys
            item_keys = [key for key in obj.keys() if key.startswith('Item')]

            # Loop through each Item key and add it to the YAML data dictionary
            for item_key in item_keys:

                item_num = item_key.replace('Item', '')
                if obj[item_key] and obj[item_key].strip():
                    yaml_data[table_name][item_key] = {'Name': obj[item_key]}
            continue

        if yaml_data.get(table_name) is None:
            print(f"{key_type} entry exists without a base table for {table_name}")
            continue

        item_keys = [key for key in obj.keys() if key.startswith('Item')]

        # Call the function to process item keys
        process_item_keys(obj, table_name, item_keys, yaml_data, key_type)

    # Convert the YAML data to a string
    yaml_string = yaml.dump(yaml_data, default_flow_style=False)

    # Replace the input file extension with '.yml'
    output_filename = filename.replace('.json', '.yml')

    # Write the YAML string to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write(yaml_string)

    print(f"YAML data has been written to {output_filename}")

if __name__ == '__main__':
    main()