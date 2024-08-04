import glob
import json
import os
import sys
# import re
# from ruamel.yaml import YAML
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
   # yaml = YAML(typ='safe')
    directory = sys.argv[1]

    # Read price_data from file
    prices_filename = os.path.join(directory, "prices.json")

    with open(prices_filename, "r", encoding="utf8") as prices_file:
        price_data = json.load(prices_file)
    price_list = {}
    for item_price in price_data:
        price_list[item_price['ItemId']] = {}
        price_list[item_price['ItemId']]['Price'] = item_price['Price']
        price_list[item_price['ItemId']]['ItemName'] = item_price['ItemName']

    master_item_defs_filename = os.path.join(directory, "MasterItemDefinitions", "MasterItemDefinitions_Crafting.json")

    with open(master_item_defs_filename, "r", encoding="utf8") as master_item_defs_file:
        master_item_defs_data = json.load(master_item_defs_file)

    master_item_defs_list = {}
    for master_item_def in master_item_defs_data:
        master_item_defs_list[master_item_def['ItemID']] = {}
        master_item_defs_list[master_item_def['ItemID']]['Name'] = master_item_def['Name']

    game_events_filename = os.path.join(directory, "GameEventData", "(Jump Top of Creatures).json")

    with open(game_events_filename, "r", encoding="utf8") as game_events_file:
        game_event_data = json.load(game_events_file)

    game_event_list = {}
    for game_event in game_event_data:

        game_event_list[game_event['EventID']] = {}
        game_event_list[game_event['EventID']]['TerritoryStanding'] = game_event['TerritoryStanding']
        game_event_list[game_event['EventID']]['CurrencyReward'] = game_event['CurrencyReward']

    tb_missions_filename = os.path.join(directory, "MissionData", "TerritoryProgressionMissions.json")

    with open(tb_missions_filename, "r", encoding="utf8") as tb_missions_file:
        tbmission_data = json.load(tb_missions_file)

    tbmission_list = {}
    for tb_mission in tbmission_data:

        tbmission_list[tb_mission['MissionID']] = {}
        tbmission_list[tb_mission['MissionID']]['SuccessGameEventIdOverride'] = tb_mission['SuccessGameEventIdOverride']
        tbmission_list[tb_mission['MissionID']]['TaskHaveAndReturnItemsOverride'] = tb_mission['TaskHaveAndReturnItemsOverride']
        tbmission_list[tb_mission['MissionID']]['TaskHaveAndReturnItemsQtyOverride'] = tb_mission['TaskHaveAndReturnItemsQtyOverride']
        tbmission_list[tb_mission['MissionID']]['TitleOverride'] = tb_mission['TitleOverride']

    weaponrecipes_filename = os.path.join(directory, "CraftingRecipeData", "CraftingRecipesWeapon.json")

    with open(weaponrecipes_filename, "r", encoding="utf8") as weaponrecipes_file:
        weaponrecipe_data = json.load(weaponrecipes_file)

    recipe_list = {}
    for weaponrecipe in weaponrecipe_data:

        recipe_list[weaponrecipe['RecipeID']] = {}
        recipe_list[weaponrecipe['RecipeID']]['Ingredient1'] = weaponrecipe['Ingredient1']
        recipe_list[weaponrecipe['RecipeID']]['Qty1'] = weaponrecipe['Qty1']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient2'] = weaponrecipe['Ingredient2']
        recipe_list[weaponrecipe['RecipeID']]['Qty2'] = weaponrecipe['Qty2']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient3'] = weaponrecipe['Ingredient3']
        recipe_list[weaponrecipe['RecipeID']]['Qty3'] = weaponrecipe['Qty3']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient4'] = weaponrecipe['Ingredient4']
        recipe_list[weaponrecipe['RecipeID']]['Qty4'] = weaponrecipe['Qty4']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient5'] = weaponrecipe['Ingredient5']
        recipe_list[weaponrecipe['RecipeID']]['Qty5'] = weaponrecipe['Qty5']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient6'] = weaponrecipe['Ingredient6']
        recipe_list[weaponrecipe['RecipeID']]['Qty6'] = weaponrecipe['Qty6']
        recipe_list[weaponrecipe['RecipeID']]['Ingredient7'] = weaponrecipe['Ingredient7']
        recipe_list[weaponrecipe['RecipeID']]['Qty7'] = weaponrecipe['Qty7']

    armorrecipes_filename = os.path.join(directory, "CraftingRecipeData", "CraftingRecipesArmorer.json")

    with open(armorrecipes_filename, "r", encoding="utf8") as armorrecipes_file:
        armorrecipe_data = json.load(armorrecipes_file)

    for armorrecipe in armorrecipe_data:

        recipe_list[armorrecipe['RecipeID']] = {}
        recipe_list[armorrecipe['RecipeID']]['Ingredient1'] = armorrecipe['Ingredient1']
        recipe_list[armorrecipe['RecipeID']]['Qty1'] = armorrecipe['Qty1']
        recipe_list[armorrecipe['RecipeID']]['Ingredient2'] = armorrecipe['Ingredient2']
        recipe_list[armorrecipe['RecipeID']]['Qty2'] = armorrecipe['Qty2']
        recipe_list[armorrecipe['RecipeID']]['Ingredient3'] = armorrecipe['Ingredient3']
        recipe_list[armorrecipe['RecipeID']]['Qty3'] = armorrecipe['Qty3']
        recipe_list[armorrecipe['RecipeID']]['Ingredient4'] = armorrecipe['Ingredient4']
        recipe_list[armorrecipe['RecipeID']]['Qty4'] = armorrecipe['Qty4']
        recipe_list[armorrecipe['RecipeID']]['Ingredient5'] = armorrecipe['Ingredient5']
        recipe_list[armorrecipe['RecipeID']]['Qty5'] = armorrecipe['Qty5']
        recipe_list[armorrecipe['RecipeID']]['Ingredient6'] = armorrecipe['Ingredient6']
        recipe_list[armorrecipe['RecipeID']]['Qty6'] = armorrecipe['Qty6']
        recipe_list[armorrecipe['RecipeID']]['Ingredient7'] = armorrecipe['Ingredient7']
        recipe_list[armorrecipe['RecipeID']]['Qty7'] = armorrecipe['Qty7']

#iterate over the townboard missions
    # If they have a direct ingredient, calculate the gold per territory standing
    # if their ingredient is a work order, calculate the total cost of the workorder into gold per standing.
    for tbmission in tbmission_list.keys():
        foo = tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']
        if tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride'].lower() in price_list.keys():
            tbmission_list[tbmission]['Cost'] = float(price_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride'].lower()]['Price']) * float(tbmission_list[tbmission]['TaskHaveAndReturnItemsQtyOverride'])
            tbmission_list[tbmission]['Standing'] = float(game_event_list[tbmission_list[tbmission]['SuccessGameEventIdOverride']]['TerritoryStanding'])
            tbmission_list[tbmission]['StandingPerGold'] = tbmission_list[tbmission]['Standing'] / tbmission_list[tbmission]['Cost']
    #TODO: Get the mission name
        if tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride'] in recipe_list.keys():
            #TODO make this not hardcoded
            # relevant_keys = sorted(
            #     (key for key in recipe_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']].keys() if key.startswith(('Qty', 'Ingredient'))),
            #     key=lambda x: int(''.join(filter(str.isdigit, x)))
            # )
            tbmission_list[tbmission]['Cost'] = 0
            for i in range(1, 8):
                qty_key = f"Qty{i}"
                ingredient_key = f"Ingredient{i}"
                if type(recipe_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']][qty_key]) is int:
                    ingredient_ = recipe_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']][ingredient_key]
                    if ingredient_.lower() in price_list.keys():
                     tbmission_list[tbmission]['Cost'] += float(price_list[ingredient_.lower()]['Price']) * float(recipe_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']][qty_key])
            tbmission_list[tbmission]['Standing'] = float(game_event_list[tbmission_list[tbmission]['SuccessGameEventIdOverride']]['TerritoryStanding'])
            tbmission_list[tbmission]['StandingPerGold'] = tbmission_list[tbmission]['Standing'] / tbmission_list[tbmission]['Cost']
        if tbmission_list[tbmission].get('StandingPerGold') is not None:
            print(f"{tbmission_list[tbmission]['TitleOverride']},{master_item_defs_list[tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']]['Name']},{tbmission_list[tbmission]['TaskHaveAndReturnItemsOverride']},{round(tbmission_list[tbmission]['Cost'],2)},{round(tbmission_list[tbmission]['StandingPerGold'],2)}")



    #the git repo I use splits the overly large loot bucket file into two to fit it into git.
    lootbuckets_filename1 = os.path.join(directory, "LootBucketData", "LootBuckets-split-00.json")
    # lootbuckets_filename2 = os.path.join(directory, "LootBucketData", "LootBuckets-split-01.json")
    #
    # # Read lootbuckets_data from split files
    # with open(lootbuckets_filename1, "r", encoding="utf8") as lootbuckets_file1:
    #     lbdata1 = lootbuckets_file1.read()
    #
    # with open(lootbuckets_filename2, "r", encoding="utf8") as lootbuckets_file2:
    #     lbdata2 = lootbuckets_file2.read()
    #
    # lbdata1 += lbdata2
    # loot_buckets_data = json.loads(lbdata1)
    # loot_buckets = {}
    # loot_bucket_names = {}
    # row_num = 0
    # for loot_bucket_obj in loot_buckets_data:
    #     row_num += 1
    #     for key in loot_bucket_obj.keys():
    #         if key.startswith("Item") and key[4:].isdigit():
    #             item_num = int(key[4:])
    #             if loot_bucket_obj['RowPlaceholders'] == "FIRSTROW":
    #                 loot_bucket_names[f'{item_num}'] = loot_bucket_obj.get(f'LootBucket{item_num}')
    #
    #             item_id = loot_bucket_obj.get(key)
    #             if item_id:
    #                 item_tags = loot_bucket_obj.get(f'Tags{item_num}')
    #                 item_qty = loot_bucket_obj.get(f'Quantity{item_num}')
    #                 item_match = loot_bucket_obj.get(f'MatchOne{item_num}')
    #                 loot_bucket_name = loot_bucket_names[f'{item_num}']
    #                 if loot_bucket_name not in loot_buckets:
    #                     loot_buckets[loot_bucket_name] = {}
    #                 if row_num not in loot_buckets[loot_bucket_name]:
    #                     loot_buckets[loot_bucket_name][row_num] = {}
    #                 loot_buckets[loot_bucket_name][row_num]['item_id'] = item_id
    #                 loot_buckets[loot_bucket_name][row_num]['tags'] = item_tags
    #                 loot_buckets[loot_bucket_name][row_num]['qty'] = item_qty
    #                 loot_buckets[loot_bucket_name][row_num]['match'] = item_match
    #
    # loottables_filename = os.path.join(directory, "LootTablesData", "LootTables.yml")
    #
    #
    # # Read loottables_data from file
    # with open(loottables_filename, "r", encoding="utf8") as loottables_file:
    #     loot_tables_data = yaml.load(loottables_file)
    #
    #
    # postCapKeys = [key for key in loot_tables_data.keys() if key.startswith('PostCap') and not key.endswith('Gypsum')]
    # # Loop through the loot buckets and process PostCap ones.
    # aptitude_crate_values = {}
    #
    # for postcap_table in postCapKeys:
    #     aptitude_crate_values[postcap_table] = {}
    #     postcap_loottable = loot_tables_data[postcap_table]
    #     for item_key in postcap_loottable.keys():
    #         if item_key.startswith('Item'):
    #             chance_factor = (postcap_loottable['MaxRoll'] - int(postcap_loottable[item_key]['Threshold'])) / postcap_loottable['MaxRoll']
    #             qty = avg_qty(postcap_loottable[item_key]['Qty'])
    #             if postcap_loottable[item_key]['Name'].startswith('['):
    #                 bucket = re.sub(r'\[.*?\]', '', postcap_loottable[item_key]['Name'])
    #                 bucket_contents = loot_buckets[bucket]
    #                 tagged_bucket = {}
    #                 for bucket_entry_key in bucket_contents.keys():
    #                     bucket_entry_tags = bucket_contents[bucket_entry_key]['tags'].split(',')
    #                     if postcap_table in bucket_entry_tags:
    #                         tagged_bucket[bucket_entry_key] = bucket_contents[bucket_entry_key]
    #                 for tagged_bucket_entry_key in tagged_bucket.keys():
    #                         bucket_qty = avg_qty(str(bucket_contents[tagged_bucket_entry_key]['qty']))
    #                         bucket_chance = 1/len(tagged_bucket.keys())
    #                         item_name = bucket_contents[tagged_bucket_entry_key]['item_id'].lower()
    #                         aptitude_crate_values[postcap_table][item_name] = {}
    #                         item_price = price_list.get(item_name, {}).get('Price', 0)
    #                         item_value = chance_factor * qty * bucket_qty * bucket_chance * float(item_price)
    #                         aptitude_crate_values[postcap_table][item_name]['value'] = item_value
    #                         aptitude_crate_values[postcap_table][item_name]['price'] = item_price
    #                         if item_value > 0:
    #                           aptitude_crate_values[postcap_table][item_name]['variance'] = float(item_price)/item_value
    #             else:
    #                 item_name = postcap_loottable[item_key]['Name'].lower()
    #                 aptitude_crate_values[postcap_table][item_name] = {}
    #                 item_price = price_list[item_name]['Price']
    #                 item_value = chance_factor * qty * float(item_price)
    #                 aptitude_crate_values[postcap_table][item_name]['value'] = item_value
    #                 aptitude_crate_values[postcap_table][item_name]['price'] = item_price
    #                 if item_value > 0:
    #                     aptitude_crate_values[postcap_table][item_name]['variance'] = float(item_price) / item_value
    # aptitude_crate_prices = defaultdict(int)
    # for crate in aptitude_crate_values.keys():
    #     total_value = 0
    #     variance = 0
    #     for treasure in aptitude_crate_values[crate].keys():
    #         total_value += aptitude_crate_values[crate][treasure]['value']
    #         item_price = float(price_list.get(treasure, {}).get('Price', 0))
    #         # print(f"{crate} {treasure} {item_price} {aptitude_crate_values[crate][treasure]}")
    #         if aptitude_crate_values[crate][treasure]['value'] > 0:
    #             variance += (item_price/aptitude_crate_values[crate][treasure]['value']) * item_price
    #     if len(aptitude_crate_values[crate].keys()) > 0:
    #         variance = variance / len(aptitude_crate_values[crate].keys())
    #     base_key = ''.join(crate.rsplit('T', 1)[0] + crate.rsplit('T', 1)[1][1:])
    #
    #     pretty_round = round(total_value, 2)
    #     aptitude_crate_prices[base_key] += pretty_round
    #
    #     #print(f"{crate},{pretty_round}, {variance}")
    # for aptitude_crate in aptitude_crate_prices:
    #     print(f"{aptitude_crate},{round(aptitude_crate_prices[aptitude_crate],2)}")


if __name__ == '__main__':
    main()
