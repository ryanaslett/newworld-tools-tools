# newworld-tools-tools
Contains various python utilities for extracting/mining/reformatting data from the newworld-tools repository.

loot.py will reformat loot tables files into two formats, condensed yaml (good for feeding other tools), and condensed
yaml with fixed width loot tables embedded (much better for comparing diffs) Feed it the filename you want reformated,
(like LootTables.json) and it will write out LootTables.yml as well as LootTables_fixedwidth.yml.

lootbuckets.py will reformat loot buckets files into two formats, condensed yaml (good for feeding other tools), and condensed
yaml with fixed width loot tables embedded (much better for comparing diffs) Feed it the filename you want reformated,
(like LootBuckets.json) and it will write out LootBuckets.yml as well as LootTables_fixedwidth.yml.

perkviolators.py scans the MasterItemDefinitions and checks the perk labels of all items with pre-defined perks. If any
item has multiples of the same label in its definition it links that item to the loot buckets it appears in. This is 
handy for finding one type of "special" item that you cannot acquire any other way.
