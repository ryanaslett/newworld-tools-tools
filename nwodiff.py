#!/usr/bin/env python

import sys
import pydevd_pycharm
import json
import os
import re
from rich import print
from rich.console import Console

#pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)


def ends_with_sci_notation(s):
    # This regex looks for a pattern like 'E-' followed by one or more digits at the end of the string
    return bool(re.search(r'E-\d+$', s))


def main():
    if len(sys.argv) != 3:
        print("Usage: nwodiff.py <file1> <file2>")
        sys.exit(1)
    console = Console(force_terminal=True, highlight=False)
    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    skip_config = os.environ.get('SKIP_FIELDS', '')
    display_new = os.environ.get('SHOW_NEW', '')
    skipped_field_list = skip_config.split(',') if skip_config else []

    if file1_path == 'nul':
        print(f"New File: {file2_path}")
    if file2_path == 'nul':
        print(f"Deleted File: {file1_path}")
    if not file1_path.endswith('.json') or not file2_path.endswith('.json'):
        # print("Both files should be .json files")
        sys.exit(1)

    print(f"\n\n[blue bold]{file2_path}")

    with open(file1_path, 'r', encoding="utf8") as file1, open(file2_path, 'r', encoding="utf8") as file2:
        old_data = json.loads(file1.read())
        new_data = json.loads(file2.read())

        # Get the key name that defines the unique object identifier. This is assumed to be the first line in each object
        object_key_old = list(set(list(item.keys())[0] for item in old_data))
        object_key_new = list(set(list(item.keys())[0] for item in new_data))

        # Check if there is more than one object key for some fucking reason
        if len(object_key_new) > 1:
            print(f"- Fuckin A More than one object key")

        # Check if the object keys changed:
        if object_key_new[0] != object_key_old[0]:
            print(f"- Fuckin A the object keys changed")

        keys_list1 = set(key for d in old_data for key in d.keys())
        keys_list2 = set(key for d in new_data for key in d.keys())

        # Find added and removed keys
        added_keys = keys_list2 - keys_list1
        removed_keys = keys_list1 - keys_list2

        # if added_keys:
        #     print("Added keys:", added_keys)
        if removed_keys:
            print(f"[red]Removed keys:{removed_keys}[/red]")

        old_data_dict = {f"{list(item.keys())[0]}_{item[list(item.keys())[0]]}": item for item in old_data}
        new_data_dict = {f"{list(item.keys())[0]}_{item[list(item.keys())[0]]}": item for item in new_data}


        differences = []
        adds = []

        path = ""

        # Check for differences in key presence
        for k in old_data_dict:
            if k not in new_data_dict:
                differences.append(f"[red]{path + '.' + k if path else k} [/red]has been deleted")

        for k in new_data_dict:
            if k not in old_data_dict:
                # differences.append(f"{path + '.' + k if path else k} Added")
                filtered_dict = {key: value for key, value in new_data_dict.get(k).items() if value not in [None, ""]}
                adds.append(f"\n[green]New Object:[/green] [green bold]{k}[/green bold]")
                if display_new:
                    for json_key in filtered_dict:
                        adds.append(f"\t[green]{json_key}[/green] : [green bold] {filtered_dict[json_key]}")

                # print(json.dumps(filtered_dict, indent=4))
            else:
                new_object = new_data_dict[k]
                old_object = old_data_dict[k]
                changes = []
                for field in new_object:

                    if field in added_keys:
                         if new_object[field] is not None and new_object[field] != '':
                             changes.append(f"Added field {field}:{new_object[field]}")
                             #pass
                    else:
                        if isinstance(new_object[field], str) and ends_with_sci_notation(new_object[field]):
                            new_object[field] = format(float(new_object[field]), '.6f')
                        if isinstance(old_object[field], str) and ends_with_sci_notation(old_object[field]):
                            old_object[field] = format(float(old_object[field]), '.6f')
                        if new_object[field] != old_object[field] and not ((new_object[field] == '' and old_object[field] is None) or (new_object[field] is None and old_object[field] == '') or str(new_object[field]) == str(old_object[field])):
                            # Ignore changes
                            if field not in skipped_field_list:
                                changes.append(f"\t{field} [red strike italic]{old_object[field]}[/]:right_arrow: [bold green]{new_object[field]}[/]")
                if changes:
                    console.print()
                    changes.sort()
                    changes.insert(0, f"[dim cyan]{k}:")
                    for change in changes:
                        console.print(change)
        #adds.sort()
        for new_objects in adds:
            console.print(new_objects)





        for difference in differences:
            print(difference)

if __name__ == "__main__":
    main()