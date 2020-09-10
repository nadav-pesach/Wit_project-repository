import os
import pathlib
from pathlib import Path
import shutil
import sys


from my_wit_project import my_wit_tools, Status


def checkout():
    current = os.getcwd()
    dst = my_wit_tools.find_parent_wit(current)
    delta = Path(current).relative_to(Path(dst))
    if dst:
        changes_to_be_committed, changes_not_staged_for_commit, untracked_files = Status.status()
        if changes_to_be_committed or changes_not_staged_for_commit:
            print('failed')
        else:
            wit_dst = os.path.join(dst, '.wit')
            check = sys.argv[2]
            if my_wit_tools.check_commit_branch(check, wit_dst):
                with open(os.path.join(wit_dst, 'activated.txt'), "w+") as my_file:
                    my_file.writelines(check)
            else:
                with open(os.path.join(wit_dst, 'activated.txt'), "w+") as my_file:
                    my_file.writelines('')
                commit_id_name = check
                if 'master' == commit_id_name:
                    commit_id_name = my_wit_tools.pre_master(wit_dst)
                    if not commit_id_name:
                        raise
                commit_id = os.path.join(wit_dst, 'images', commit_id_name, delta)
                for filepath2 in pathlib.Path(commit_id).glob('**/*'):
                    check = True
                    for filepath in pathlib.Path(current).glob('**/*'):
                        if Path(filepath.absolute()).relative_to(current) == Path(filepath2.absolute()).relative_to(commit_id):
                            check = False
                            if os.path.isfile(filepath.absolute()):
                                if os.stat(filepath2).st_mtime - os.stat(filepath).st_mtime > 1:
                                    shutil.copy2(filepath2, filepath)
                    if check and Path(filepath2.absolute()).relative_to(commit_id) not in untracked_files and os.path.isfile(filepath2.absolute()):
                        copy_to = Path(os.path.join(dst, delta, Path(filepath2.absolute()).relative_to(commit_id)))
                        os.makedirs(copy_to.parent, exist_ok=True)
                        try:
                            shutil.copy2(filepath2, copy_to)
                        except FileNotFoundError:
                            print('FileNotFoundError')
                staging_area_dst = os.path.join(wit_dst, 'staging_area')
                shutil.rmtree(staging_area_dst, ignore_errors=True)
                try:
                    os.makedirs(staging_area_dst, exist_ok=True)
                except PermissionError:
                    print('PermissionError')
                commit_id = os.path.join(wit_dst, 'images', commit_id_name)
                if os.path.isdir(commit_id):
                    try:
                        shutil.copytree(commit_id, staging_area_dst, dirs_exist_ok=True)
                    except FileNotFoundError:
                        print('FileNotFoundError')
                else:
                    try:
                        shutil.copy2(commit_id, staging_area_dst)
                    except FileNotFoundError:
                        print('FileNotFoundError')
                with open(os.path.join(wit_dst, 'references.txt'), "r") as my_file:
                    lines = my_file.readlines()
                lines[0] = f'HEAD={commit_id_name}\n'
                with open(os.path.join(wit_dst, 'references.txt'), "w") as my_file:
                    my_file.writelines(lines)
# Reupload