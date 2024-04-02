import json
import sys
from ruamel.yaml.scalarstring import PreservedScalarString
from ruamel.yaml import YAML

def process_fixed_width_item_keys(loot_buckets, yaml_data):
    # Define the fixed width column widths
    item_width: int = 4
    tags_width: int = 25
    qty_width: int = 10
    match_width: int = 10
    lootbias_width: int = 5
    odds_width: int = 4
    name_width: int = 72  # because `Schematic_House_HousingItem_Table_Settler_Decor_Garden_PicnicTable01`

    # Loop through each Item key and add it to the YAML data dictionary

    for loot_bucket_name, loot_bucket_contents in loot_buckets.items():
        items_string = ""
        item_keys = [key for key in loot_bucket_contents.keys()]
        for item_key in item_keys:

            item_id = loot_bucket_contents[item_key]['item_id']
            item_tags = loot_bucket_contents[item_key]['tags']
            item_qty = loot_bucket_contents[item_key]['qty']
            item_match = loot_bucket_contents[item_key]['match']
            item_lootbias_disabled = loot_bucket_contents[item_key]['lootbiasdisabled']
            item_odds = loot_bucket_contents[item_key]['odds']
            item_string = f'{str(item_key).ljust(item_width)} {item_id.ljust(name_width)} {str(item_qty).rjust(qty_width)} {str(item_match).ljust(match_width)} {str(item_lootbias_disabled).ljust(lootbias_width)} {str(item_odds).rjust(odds_width)} {item_tags.ljust(tags_width)}  \n'
            items_string += item_string

    # Construct the multi-line string for the Item fields
        items_output = f"Idx  ItemId{' ' * (name_width - 6)} {' ' * (qty_width - 3)}Qty MatchOne{' ' * (match_width - 8)} LBDis Odds Tags\n{'_' * (10 + name_width + tags_width + qty_width + match_width + lootbias_width + odds_width)}\n{items_string}"
        yaml_data[loot_bucket_name] = {}
        yaml_data[loot_bucket_name]['Contents'] = PreservedScalarString(items_output)

def main():
    # Check that a filename was provided
    if len(sys.argv) < 2:
        print("Please provide the filename of the input JSON file as a command-line argument.")
        sys.exit()

    # Load the JSON data from the specified file
    filename = sys.argv[1]
    with open(filename, 'r', encoding="utf8") as f:
        loot_buckets_data = json.load(f)

    # Create a dictionary for the output YAML data
    yaml_data = {}

    # Loop through each JSON object and populate the YAML data dictionary
    loot_buckets = {}
    loot_bucket_names = {}
    row_num = 0
    for loot_bucket_obj in loot_buckets_data:
        row_num += 1
        for key in loot_bucket_obj.keys():
            if key.startswith("Item") and key[4:].isdigit():
                item_num = int(key[4:])
                if loot_bucket_obj['RowPlaceholders'] == "FIRSTROW":
                    loot_bucket_names[f'{item_num}'] = loot_bucket_obj.get(f'LootBucket{item_num}')

                item_id = loot_bucket_obj.get(key)
                if item_id:
                    item_tags = loot_bucket_obj.get(f'Tags{item_num}')
                    item_qty = loot_bucket_obj.get(f'Quantity{item_num}')
                    loot_biasing_disabled = loot_bucket_obj.get(f'LootBiasingDisabled{item_num}')
                    odds = loot_bucket_obj.get(f'Odds{item_num}')
                    item_match = loot_bucket_obj.get(f'MatchOne{item_num}')
                    loot_bucket_name = loot_bucket_names[f'{item_num}']
                    if loot_bucket_name not in loot_buckets:
                        loot_buckets[loot_bucket_name] = {}
                    if row_num not in loot_buckets[loot_bucket_name]:
                        loot_buckets[loot_bucket_name][row_num] = {}
                    loot_buckets[loot_bucket_name][row_num]['item_id'] = item_id
                    loot_buckets[loot_bucket_name][row_num]['tags'] = item_tags
                    loot_buckets[loot_bucket_name][row_num]['qty'] = item_qty
                    loot_buckets[loot_bucket_name][row_num]['match'] = item_match
                    loot_buckets[loot_bucket_name][row_num]['lootbiasdisabled'] = loot_biasing_disabled
                    loot_buckets[loot_bucket_name][row_num]['odds'] = odds

    process_fixed_width_item_keys(loot_buckets, yaml_data)

    # Write the YAML data to file
    yaml = YAML()
    with open('output.yml', 'w', encoding="utf8") as f:
        yaml.dump(yaml_data, f)

if __name__ == '__main__':
    main()
