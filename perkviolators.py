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
    item_filename = os.path.join(directory, "MasterItemDefinitions", "MasterItemDefinitions_Named.json")
    perk_filename = os.path.join(directory, "PerkData", "ItemPerks.json")
    lootbuckets_filename = os.path.join(directory, "LootBucketData", "LootBuckets.json")

    # Read items from file
    with open(item_filename, "r") as items_file:
        items = json.load(items_file)

    # Read perks from file
    with open(perk_filename, "r") as perks_file:
        perks_list = json.load(perks_file)
        # Convert the list of perks to a dictionary for easier access
        perks = {perk["PerkID"]: perk["ExclusiveLabels"] for perk in perks_list if
                 "_Gem_" not in perk["PerkID"] and "_Stat_" not in perk["PerkID"]}

    # Read lootbuckets from file
    with open(lootbuckets_filename, "r") as lootbuckets_file:
        lootbuckets = json.load(lootbuckets_file)

    # Process the data
    output_data = []
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
            output_data.append({"ItemID": item["ItemID"], "Perks": perk_data})
            print(f"https://nwdb.info/db/item/{item['ItemID']}")

    # Write the result to a file
    with open("output.json", "w") as output_file:
        json.dump(output_data, output_file, indent=2)


if __name__ == '__main__':
    main()
