import os
import sys
import json
from collections import defaultdict


def main():
    # Check that a directory was provided
    if len(sys.argv) < 2:
        print("Please provide the directory containing the input JSON files as a command-line argument.")
        sys.exit()

    directory = sys.argv[1]
    #item_filename = os.path.join(directory, "MasterItemDefinitions", "MasterItemDefinitions_Named.json")
    item_directory = os.path.join(directory, "MasterItemDefinitions")

    perk_filename = os.path.join(directory, "PerkData", "ItemPerks.json")
    lootbuckets_filename = os.path.join(directory, "LootBucketData", "LootBuckets.json")

    # Read perks from file
    with open(perk_filename, "r") as perks_file:
        perks_list = json.load(perks_file)
        # Convert the list of perks to a dictionary for easier access
        perks = {perk["PerkID"]: perk["ExclusiveLabels"] for perk in perks_list if
                 "_Gem_" not in perk["PerkID"] and "_Stat_" not in perk["PerkID"]}

    # Read lootbuckets_data from file
    with open(lootbuckets_filename, "r") as lootbuckets_file:
        loot_buckets_data = json.load(lootbuckets_file)

    loot_buckets = {}
    loot_bucket_names = {}
    for loot_bucket_obj in loot_buckets_data:
        for key in loot_bucket_obj.keys():
            if key.startswith("Item") and key[4:].isdigit():
                item_num = int(key[4:])
                if loot_bucket_obj['RowPlaceholders'] == "FIRSTROW":
                    loot_bucket_names[f'{item_num}'] = loot_bucket_obj.get(f'LootBucket{item_num}')

                item_id = loot_bucket_obj.get(key)
                if item_id:
                    item_tag = loot_bucket_obj.get(f'Tags{item_num}')
                    loot_bucket_name = loot_bucket_names[f'{item_num}']
                    if item_id not in loot_buckets:
                        loot_buckets[item_id] = {}
                    loot_buckets[item_id][loot_bucket_name] = item_tag


    # Process the data
    output_data = []
    skip_files = ["MasterItemDefinitions_Named_Depricated.json", "MasterItemDefinitions/MasterItemDefinitions_Playtest.json"]
    for filename in os.listdir(item_directory):

        if not filename.endswith(".json"):
            continue
        if filename in skip_files:
            continue
        item_filename = os.path.join(item_directory, filename)

        # Read items from file
        with open(item_filename, "r") as items_file:
            items = json.load(items_file)

        for item in items:
            perk_data = {}
            for i in range(1, 6):
                perk_key = f"Perk{i}"
                perk_id = item.get(perk_key)
                if perk_id and "_Gem_" not in perk_id and "_Stat_" not in perk_id:
                    existing_perk = perk_data.get(perk_id, None)
                    if existing_perk is None:
                      perk_data[perk_id] = perks.get(perk_id)
                #    else:
                #      print(f"https://nwdb.info/db/item/{item['ItemID']}")

            # Count the number of occurrences of each ExclusiveLabel
            label_counts = defaultdict(int)
            for label in perk_data.values():
                if label is not None:
                    sublabels = label.split("+")
                    for sublabel in sublabels:

                       if sublabel is not None:
                           label_counts[sublabel] += 1

            # Filter objects with more than one of any particular ExclusiveLabel assigned
            if any(count > 1 for count in label_counts.values()):
                loot_bucket_info = loot_buckets.get(item['ItemID'])
                if loot_bucket_info:
                    loot_bucket_string = ""
                    for loot_bucket_name, item_tag in loot_bucket_info.items():
                        loot_bucket_string += f"{loot_bucket_name}:{item_tag}, "
                    loot_bucket_string = loot_bucket_string.rstrip(", ")
                else:
                    # print(f"No loot buckets found for {item['ItemID']}")
                    loot_bucket_string = ""

                output_data.append({"ItemID": item["ItemID"], "Perks": perk_data})
                print(f"https://nwdb.info/db/item/{item['ItemID']} , Lootbucket Info; {loot_bucket_string}, From: {filename}")

    # Write the result to a file
    with open("output.json", "w") as output_file:
        json.dump(output_data, output_file, indent=2)


if __name__ == '__main__':
    main()
