from datetime import datetime, timezone
import os
import sys


from my_wit_project import Add, my_wit_tools


def commit(message=None):
    # made credit to add even tho it completely different that source
    # toke me 2 days and 1 day rest and coming back on the 4th day to finish this oh god
    dst = my_wit_tools.find_parent_wit(os.getcwd())
    wit_dst = os.path.join(dst, '.wit')
    images_dst = os.path.join(wit_dst, 'images')
    staging_area_dst = os.path.join(wit_dst, 'staging_area')
    pre_file_name = my_wit_tools.pre_file(wit_dst)
    new_file_name = my_wit_tools.get_random_file_name(40, images_dst)
    d = os.path.join(images_dst, new_file_name)
    os.mkdir(d)
    print("Successfully created the directory %s " % d)
    try:
        with open(os.path.join(wit_dst, 'references.txt'), "r") as my_file:
            lines = my_file.readlines()
    except FileNotFoundError:
        with open(os.path.join(wit_dst, 'references.txt'), "w") as my_file:
            lines[0] = f'HEAD={new_file_name}\nmaster={new_file_name}'
    branch_name = my_wit_tools.active_branch(wit_dst)[0]
    branch_id = my_wit_tools.branch_id_number(wit_dst, branch_name)
    print(branch_id, branch_name)
    if branch_name and pre_file_name == branch_id:
        my_wit_tools.update_references(my_wit_tools.active_branch(wit_dst)[0], new_file_name, lines, wit_dst)
    else:
        lines[0] = f'HEAD={new_file_name}\n'
        with open(os.path.join(wit_dst, 'references.txt'), "w") as my_file:
            my_file.writelines(lines)
    if message:
        the_message = message
    else:
        the_message = sys.argv[3:]
    if isinstance(the_message, list):
        the_message = ' '.join(the_message)
    lines = [f'parent = {pre_file_name}', '\n', f'date = {datetime.now(timezone.utc).astimezone()}', '\n',
             f'message = {the_message}']
    with open(f"{d}.txt", "a") as my_file:
        my_file.writelines(lines)
    Add.add(staging_area_dst, d)
    print('Successfully created backup at %s ' % d)
# Reupload