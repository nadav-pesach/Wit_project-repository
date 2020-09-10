import os
import sys


from my_wit_project import my_wit_tools


def wit_branch():
    dst = my_wit_tools.find_parent_wit(os.getcwd())
    wit_dst = os.path.join(dst, '.wit')
    project_name = sys.argv[2]
    with open(os.path.join(wit_dst, 'references.txt'), "a") as my_file:
        my_file.writelines(f'{project_name}={my_wit_tools.pre_file(wit_dst)}\n')
