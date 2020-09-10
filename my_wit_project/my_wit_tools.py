import os
from pathlib import Path
import random


def get_random_file_name(length, dst):
    letters = '1234567890abcdef'
    result_str = ''.join(random.choice(letters) for _ in range(length))
    d = os.path.join(dst, result_str)
    if not os.path.exists(d):
        return result_str
    return get_random_file_name(length, dst)


def find_parent_wit(dst):
    while not os.path.exists(os.path.join(dst, '.wit')):
        if dst == Path(dst).parent and not os.path.exists(os.path.join(dst, '.wit')):
            raise RuntimeError(f"'{os.path.join(dst, '.wit')}' not found")
        dst = Path(dst).parent
    return dst


def pre_file(wit_dst):
    with open(os.path.join(wit_dst, 'references.txt'), "a+") as my_file:
        my_file.seek(0)
        lines = my_file.readlines()
        if lines:
            for line in lines:
                if 'HEAD' in line:
                    pre_file_name = line[5:45]
                    return pre_file_name
    return None


def find_next_file_name(current_name, images_dst):
    try:
        with open(os.path.join(images_dst, f'{current_name}.txt'), "r") as my_file:
            lines = my_file.readlines()
    except FileNotFoundError:
        return None
    try:
        parents = lines[0][9:].split(',')
        if parents == 'None':
            return None
        if parents:
            return parents
    except UnboundLocalError:
        return None


def pre_master(wit_dst):
    with open(os.path.join(wit_dst, 'references.txt'), "a+") as my_file:
        my_file.seek(0)
        lines = my_file.readlines()
        if lines:
            for line in lines:
                if 'master' in line:
                    pre_master_name = line[7:47]
                    return pre_master_name
    return None


def check_commit_branch(check, wit_dst):
    with open(os.path.join(wit_dst, 'references.txt'), "a+") as my_file:
        my_file.seek(0)
        lines = my_file.readlines()
        if lines:
            for line in lines:
                if line.startswith(check):
                    return True
            return False


def active_branch(wit_dst):
    with open(os.path.join(wit_dst, 'activated.txt'), "r") as my_file:
        lines = my_file.readlines()
    return lines


def update_references(active_branch_name, new_file_name, lines, wit_dst):
    new_txt = []
    for line in lines:
        if line.startswith(active_branch_name):
            new_txt += [f'{active_branch_name}={new_file_name}\n']
        else:
            new_txt += [line]
    new_txt[0] = f'HEAD={new_file_name}\n'
    with open(os.path.join(wit_dst, 'references.txt'), "w+") as my_file:
        my_file.writelines(new_txt)


def branch_id_number(wit_dst, branch_name):
    with open(os.path.join(wit_dst, 'references.txt'), "r") as my_file:
        lines = my_file.readlines()
    if lines:
        for line in lines:
            if line.startswith(branch_name):
                branch_number = line[-41: -1]
                return branch_number
    return None


def my_fun_graph(pre_name, current_name, my_graph, images_dst):
    if pre_name and current_name:
        for pre in pre_name:
            for current in current_name:
                my_graph.edge(pre[0:6], current[0:6])
        pre_name = current_name
        for current in current_name:
            current_name_pre = find_next_file_name(current.rstrip('\n'), images_dst)
            my_fun_graph(pre_name, current_name_pre, my_graph, images_dst)
    return my_graph
# Reupload
