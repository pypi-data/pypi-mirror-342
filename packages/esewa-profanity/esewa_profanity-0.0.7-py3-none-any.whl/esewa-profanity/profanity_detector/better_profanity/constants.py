# -*- coding: utf-8 -*-
from io import open
from json import load
from string import ascii_letters, digits
import os
from .utils import get_complete_path_of_file

ALLOWED_CHARACTERS = set(ascii_letters)
ALLOWED_CHARACTERS.update(set(digits))
ALLOWED_CHARACTERS.update({"@", "$", "*", '"', "'"})
cwd = os.getcwd()
unicode_file_location = os.path.join(cwd,'files','json','alphabetic_unicode.json')
# Pre-load the unicode characters
with open(get_complete_path_of_file(unicode_file_location), "r") as json_file:
    ALLOWED_CHARACTERS.update(load(json_file))
