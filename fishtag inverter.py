import re

def parse_fixed_width_yaml(yaml_string):
    parsed_data = {}
    yaml_lines = yaml_string.split('\n')

    current_rarity = ''
    current_tags = []
    current_item_ids = []

    for line in yaml_lines:
        if line.startswith('Fish'):
            current_rarity = line.split(':')[0]
            parsed_data[current_rarity] = {}
        elif line.startswith('    ItemId'):
            current_tags = []
            current_item_ids = []
        elif line.startswith('    ') and line.strip():
            columns = re.split(r'\s{2,}', line.strip())
            item_id = columns[0]
            tags = columns[-1].split(',')

            if tags:
                current_tags.extend(tags)
            else:
                # ItemID without any tags, associate with all tags
                current_tags = []

            current_item_ids.append(item_id)

        # Store the current tags and associated ItemIDs
        parsed_data[current_rarity][tuple(sorted(set(current_tags)))] = current_item_ids

    return parsed_data


def generate_output(parsed_data):
    output = ''
    rarity_mapping = {
        'Common': 'Common',
        'Uncommon': 'Uncommon',
        'Rare': 'Rare',
        'Ultra': 'Ultra'
    }

    for rarity, tags_data in parsed_data.items():
        output += rarity_mapping.get(rarity, rarity) + ':\n'
        for tags, item_ids in tags_data.items():
            if not tags:
                tags_str = 'All'
            else:
                tags_str = ', '.join(sorted(tags))
            output += f'  {tags_str}:\n'
            for item_id in item_ids:
                output += f'    - {item_id}\n'

    return output


# Example usage
fixed_width_yaml = """
FishCommonSmallFresh:
  Contents: |
    ItemId                                                                          Qty MatchOne   Tags
    ________________________________________________________________________________________________________________
    FishingSalmonSmallT1                                                              1 TRUE
    FishingPikeSmallT1                                                                1 TRUE
    FishingTroutSmallT1                                                               1 TRUE       Everfall,Brightwood,Weavers,GreatCleave,Queensport,Reekwater,FirstLight 
    FishingSunfishSmallT1                                                             1 TRUE       Windsward,Everfall,Weavers,Restless,Edengrove,Reekwater,Shattered 
    FishingBassSmallT1                                                                1 TRUE       Monarchs,Everfall,Brightwood,Weavers,GreatCleave,Edengrove,Shattered 
    FishingPerchSmallT1                                                               1 TRUE       Windsward,Everfall,Brightwood,CutlassKeys,Mourning,Edengrove,Shattered,Brimstone 
"""

parsed_data = parse_fixed_width_yaml(fixed_width_yaml)
output = generate_output(parsed_data)
print(output)