import os

def get_package_location():
    curent_file_path = os.path.abspath(__file__)
    return os.path.dirname(os.path.dirname(curent_file_path))