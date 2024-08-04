import glob
import json
import os
import sys
import re
from ruamel.yaml import YAML
from collections import defaultdict


def avg_qty(s):
    # Split the string at the dash
    qty = s.split('-')

    if len(qty) == 1:
        return float(qty[0])
    # Convert the substrings to integers and compute the average
    avg = (int(qty[0]) + int(qty[1])) / 2

    return avg
def main():
    # Check that a directory was provided
    if len(sys.argv) < 2:
        print("Please provide the datasheet directory and path to price file")
        sys.exit()
    yaml = YAML(typ='safe')
    directory = sys.argv[1]

    #the git repo I use splits the overly large loot bucket file into two to fit it into git.
    lootbuckets_filename1 = os.path.join(directory, "LootBucketData", "LootBuckets-split-00.json")
    lootbuckets_filename2 = os.path.join(directory, "LootBucketData", "LootBuckets-split-01.json")

    # Read lootbuckets_data from split files
    with open(lootbuckets_filename1, "r", encoding="utf8") as lootbuckets_file1:
        lbdata1 = lootbuckets_file1.read()

    with open(lootbuckets_filename2, "r", encoding="utf8") as lootbuckets_file2:
        lbdata2 = lootbuckets_file2.read()

    lbdata1 += lbdata2
    loot_buckets_data = json.loads(lbdata1)
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

    loottables_filename = os.path.join(directory, "LootTablesData", "LootTables.yml")


    # Read loottables_data from file
    with open(loottables_filename, "r", encoding="utf8") as loottables_file:
        loot_tables_data = yaml.load(loottables_file)

    # Read price_data from file
    prices_filename = os.path.join(directory, "prices.json")

    with open(prices_filename, "r", encoding="utf8") as prices_file:
        price_data = json.load(prices_file)
    price_list = {}
    for item_price in price_data:
        price_list[item_price['ItemId']] = {}
        price_list[item_price['ItemId']]['Price'] = item_price['Price']
        price_list[item_price['ItemId']]['ItemName'] = item_price['ItemName']
    postCapKeys = [key for key in loot_tables_data.keys() if key.startswith('PostCap') and not key.endswith('Gypsum')]
    # Loop through the loot buckets and process PostCap ones.
    aptitude_crate_values = {}

    for postcap_table in postCapKeys:
        aptitude_crate_values[postcap_table] = {}
        postcap_loottable = loot_tables_data[postcap_table]
        for item_key in postcap_loottable.keys():
            if item_key.startswith('Item'):
                chance_factor = (postcap_loottable['MaxRoll'] - int(postcap_loottable[item_key]['Threshold'])) / postcap_loottable['MaxRoll']
                qty = avg_qty(postcap_loottable[item_key]['Qty'])
                if postcap_loottable[item_key]['Name'].startswith('['):
                    bucket = re.sub(r'\[.*?\]', '', postcap_loottable[item_key]['Name'])
                    bucket_contents = loot_buckets[bucket]
                    tagged_bucket = {}
                    for bucket_entry_key in bucket_contents.keys():
                        bucket_entry_tags = bucket_contents[bucket_entry_key]['tags'].split(',')
                        if postcap_table in bucket_entry_tags:
                            tagged_bucket[bucket_entry_key] = bucket_contents[bucket_entry_key]
                    for tagged_bucket_entry_key in tagged_bucket.keys():
                            bucket_qty = avg_qty(str(bucket_contents[tagged_bucket_entry_key]['qty']))
                            bucket_chance = 1/len(tagged_bucket.keys())
                            item_name = bucket_contents[tagged_bucket_entry_key]['item_id'].lower()
                            aptitude_crate_values[postcap_table][item_name] = {}
                            item_price = price_list.get(item_name, {}).get('Price', 0)
                            item_value = chance_factor * qty * bucket_qty * bucket_chance * float(item_price)
                            aptitude_crate_values[postcap_table][item_name]['value'] = item_value
                            aptitude_crate_values[postcap_table][item_name]['price'] = item_price
                            if item_value > 0:
                              aptitude_crate_values[postcap_table][item_name]['variance'] = float(item_price)/item_value
                else:
                    item_name = postcap_loottable[item_key]['Name'].lower()
                    aptitude_crate_values[postcap_table][item_name] = {}
                    item_price = price_list[item_name]['Price']
                    item_value = chance_factor * qty * float(item_price)
                    aptitude_crate_values[postcap_table][item_name]['value'] = item_value
                    aptitude_crate_values[postcap_table][item_name]['price'] = item_price
                    if item_value > 0:
                        aptitude_crate_values[postcap_table][item_name]['variance'] = float(item_price) / item_value
    aptitude_crate_prices = defaultdict(int)
    for crate in aptitude_crate_values.keys():
        total_value = 0
        variance = 0
        for treasure in aptitude_crate_values[crate].keys():
            total_value += aptitude_crate_values[crate][treasure]['value']
            item_price = float(price_list.get(treasure, {}).get('Price', 0))
            # print(f"{crate} {treasure} {item_price} {aptitude_crate_values[crate][treasure]}")
            if aptitude_crate_values[crate][treasure]['value'] > 0:
                variance += (item_price/aptitude_crate_values[crate][treasure]['value']) * item_price
        if len(aptitude_crate_values[crate].keys()) > 0:
            variance = variance / len(aptitude_crate_values[crate].keys())
        base_key = ''.join(crate.rsplit('T', 1)[0] + crate.rsplit('T', 1)[1][1:])

        pretty_round = round(total_value, 2)
        aptitude_crate_prices[base_key] += pretty_round

        #print(f"{crate},{pretty_round}, {variance}")
    for aptitude_crate in aptitude_crate_prices:
        print(f"{aptitude_crate},{round(aptitude_crate_prices[aptitude_crate],2)}")


if __name__ == '__main__':
    main()
