import os
from pathlib import Path
import shutil
import sys


from my_wit_project import my_wit_tools


def add(src, d=None):
    # credit atzz
    # credit Mital Vora
    # https://stackoverflow.com/a/12514470
    # https://stackoverflow.com/a/13814557
    s = os.path.join(os.getcwd(), src)
    dst = my_wit_tools.find_parent_wit(s)
    x = os.path.join(os.getcwd(), sys.argv[2])
    if os.path.isfile(x):
        path = Path(x).parent.relative_to(Path(dst))
        dst = os.path.join(dst, '.wit', 'staging_area', path)
        os.makedirs(dst, exist_ok=True)
        try:
            shutil.copy2(os.path.join(os.getcwd(), sys.argv[2]), dst)
        except FileNotFoundError:
            print('FileNotFoundError, 0')
    else:
        if d:
            dst = os.path.join(dst, d)
            s = src
        else:
            path = Path(s).relative_to(Path(dst))
            dst = os.path.join(dst, '.wit', 'staging_area', path)
            os.makedirs(dst, exist_ok=True)
        if os.path.isdir(s):
            try:
                shutil.copytree(s, dst, dirs_exist_ok=True)
            except FileNotFoundError:
                print('FileNotFoundError, 1')
        else:
            try:
                shutil.copy2(s, dst)
            except FileNotFoundError:
                print('FileNotFoundError, 2', s, dst)
# Reupload