import os
import pathlib
from pathlib import Path


from my_wit_project import my_wit_tools


def status():
    current = os.getcwd()
    place = my_wit_tools.find_parent_wit(current)
    delta = Path(current).relative_to(Path(place))
    if place:
        wit_dst = os.path.join(place, '.wit')
        pre_file_name = my_wit_tools.pre_file(wit_dst)
        if pre_file_name:
            backup_dst = os.path.join(wit_dst, 'images', pre_file_name, delta)
            staging_area_dst = os.path.join(wit_dst, 'staging_area', delta)
            changes_to_be_committed = []
            changes_not_staged_for_commit = []
            untracked_files = []
            # credit MSeifert( the 'for' line and the filepath2.absolute(), not sure if need credit for that)
            # https://stackoverflow.com/a/45960127
            for filepath2 in pathlib.Path(staging_area_dst).glob('**/*'):
                check = True
                for filepath in pathlib.Path(backup_dst).glob('**/*'):
                    check = True
                    if Path(filepath.absolute()).relative_to(backup_dst) == Path(filepath2.absolute()).relative_to(staging_area_dst):
                        check = False
                        if os.path.isfile(filepath.absolute()):
                            if os.stat(filepath2).st_mtime - os.stat(filepath).st_mtime > 1:
                                changes_to_be_committed += [Path(filepath2.absolute()).relative_to(staging_area_dst)]
                if check and os.path.isfile(filepath2.absolute()):
                    changes_to_be_committed += [Path(filepath2.absolute()).relative_to(staging_area_dst)]
            for filepath in pathlib.Path(current).glob('**/*'):
                check = True
                for filepath2 in pathlib.Path(staging_area_dst).glob('**/*'):
                    if Path(filepath.absolute()).relative_to(current) == Path(filepath2.absolute()).relative_to(staging_area_dst):
                        check = False
                        if os.path.isfile(filepath.absolute()):
                            if os.stat(filepath).st_mtime - os.stat(filepath2).st_mtime > 1:
                                changes_not_staged_for_commit += [filepath]
                if check:
                    untracked_files += [os.path.basename(filepath)]
            print('Pre_file_name: ', pre_file_name)
            print('Changes to be committed: ', [os.path.basename(filepath) for filepath in changes_to_be_committed])
            print('Changes_not_staged_for_commit: ', [os.path.basename(filepath) for filepath in changes_not_staged_for_commit])
            print('Untracked_files: ', [os.path.basename(filepath) for filepath in untracked_files])
            return changes_to_be_committed, changes_not_staged_for_commit, untracked_files
        else:
            print('No backup in system')
    else:
        print('No .wit in %s ' % place)
# Reupload