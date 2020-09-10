from filecmp import dircmp
import os
import pathlib
import shutil
import sys


from my_wit_project import Commit, my_wit_tools


def merge():
    dst = my_wit_tools.find_parent_wit(os.getcwd())
    wit_dst = os.path.join(dst, '.wit')
    images_dst = os.path.join(wit_dst, 'images')
    staging_area_dst = os.path.join(wit_dst, 'staging_area')
    branch_name = sys.argv[2]
    commit_id = os.path.join(images_dst, branch_name)
    delta = pathlib.Path(os.getcwd()).relative_to(pathlib.Path(dst))
    x = dircmp(staging_area_dst, os.path.join(images_dst, my_wit_tools.pre_file(wit_dst)))
    if x.diff_files:
        return 'Failed'
    for filepath2 in pathlib.Path(commit_id).glob('**/*'):
        check = True
        for filepath in pathlib.Path(staging_area_dst).glob('**/*'):
            if pathlib.Path(filepath.absolute()).relative_to(staging_area_dst) == pathlib.Path(filepath2.absolute()).relative_to(commit_id):
                check = False
                if os.path.isfile(filepath.absolute()):
                    if os.stat(filepath2).st_mtime - os.stat(filepath).st_mtime > 1:
                        shutil.copy2(filepath2, filepath)
        if check and os.path.isfile(
                filepath2.absolute()):
            copy_to = pathlib.Path(os.path.join(staging_area_dst, delta, pathlib.Path(filepath2.absolute()).relative_to(commit_id)))
            os.makedirs(copy_to.parent, exist_ok=True)
            try:
                shutil.copy2(filepath2, copy_to)
            except FileNotFoundError:
                print('FileNotFoundError.')
    Commit.commit(f'commit of branch merge with head {branch_name}')
# Reupload