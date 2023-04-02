import json
import sys

#import yaml
import ruamel.yaml
from ruamel.yaml.scalarstring import PreservedScalarString




def process_item_keys(obj, table_name, item_keys, yaml_data, key_type):
    for item_key in item_keys:
        if obj[item_key] and obj[item_key].strip():
            if item_key not in yaml_data[table_name]:
                yaml_data[table_name][item_key] = {}
            yaml_data[table_name][item_key].update({key_type: obj[item_key]})

def process_fixed_width_item_keys(yaml_data):
    # Define the fixed width column widths
    item_width: int = 10
    threshold_width: int = 10
    qty_width: int = 10
    name_width: int = 60

    # Loop through each Item key and add it to the YAML data dictionary

    for loot_table_id, loot_table in yaml_data.items():
        items_string = ""
        item_keys = [key for key in loot_table.keys() if key.startswith('Item')]
        for item_key in item_keys:
            item_num = item_key.replace('Item', '')

            item_name = loot_table[item_key]['Name']
            item_threshold = loot_table[item_key]['Threshold']
            item_qty = loot_table[item_key]['Qty']
            item_string = f'{item_key.ljust(item_width)} {item_threshold.rjust(threshold_width)} {item_qty.rjust(qty_width)} {item_name.ljust(name_width)}\n'
            items_string += item_string
            del(yaml_data[loot_table_id][item_key])

    # Construct the multi-line string for the Item fields
        items_output = f"Entry{' ' * (item_width - 4)}{' ' * (threshold_width - 9)} Threshold{' ' * (qty_width - 3)}Qty Name\n{'_' * (item_width + threshold_width + qty_width + name_width)}\n{items_string}"
        yaml_data[loot_table_id]['Items'] = PreservedScalarString(items_output)


def main():
    yaml = ruamel.yaml.YAML();
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.width = 1000
    yaml.preserve_quotes = True
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

    output_filename = filename.replace('.json', '.yml')

    # Write the YAML string to the output file
    with open(output_filename, 'w') as output_file:
        yaml.dump(yaml_data, output_file)

    # Convert the YAML data to a string
    process_fixed_width_item_keys(yaml_data)

    # Replace the input file extension with '.yml'
    output_filename = filename.replace('.json', '_fixedwidth.yml')

    # Write the YAML string to the output file
    with open(output_filename, 'w') as output_file:
        yaml.dump(yaml_data, output_file)

    print(f"Fixed width YAML table has been written to {output_filename}")

if __name__ == '__main__':
    main()