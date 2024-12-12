from os import listdir
from os.path import isfile, join

def get_files_list(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles
