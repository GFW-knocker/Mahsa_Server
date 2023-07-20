import os


def remove_dir(directory):
    # delete the directory
    os.system(f"rm -rf {directory}")