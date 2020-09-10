import os


def init():
    wit_dst = os.path.join(os.getcwd(), '.wit')
    paths = (wit_dst, os.path.join(wit_dst, 'images'), os.path.join(wit_dst, 'staging_area'))
    for path in paths:
        # credit https://stackabuse.com/creating-and-deleting-directories-with-python/
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
    with open(os.path.join(wit_dst, 'activated.txt'), "a") as my_file:
        my_file.writelines('master')
# Reupload