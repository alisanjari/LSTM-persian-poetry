from os import walk

PATH_POEM_FOLDER = r'D:\learning-ai\poem\molana'
PATH_ALL_POEM_FILE = r'D:\learning-ai\poem\full_molana.txt'

import os
from readfromtxt import tokenize_beyts

def merge_all_poems(read_from_folder, save_file):

    poem_files = [os.path.join(read_from_folder, f) for f in sorted(os.listdir(read_from_folder))]
    tokens = []
    for poem_file in poem_files:
        tokens = tokens + tokenize_beyts(poem_file)

    all_poems = ''
    for x in ''.join(tokens).split('\n'):
        all_poems = all_poems + '\n' + x[::-1]

    with open(save_file, 'w', encoding='utf-16') as f:
        f.write(all_poems)


read_from_folder = PATH_POEM_FOLDER
save_file = PATH_ALL_POEM_FILE
merge_all_poems(read_from_folder, save_file)