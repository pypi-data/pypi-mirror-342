import os
# from pathlib import Path
from cryptography.fernet import Fernet
from utils import get_package_location

class KeyGenerator:
    def generate(self):
        """
        Generates the Key and stores to the specific location.
        Overrides old key when new key is generated.
        """        
        key = Fernet.generate_key()
        # print(os.path.dirname(os.path.abspath(__file__)))
        cwd = get_package_location()
        file_location = os.path.join(cwd, 'files','keys', 'secret.key')
        with open(file_location, 'wb') as key_file:
            key_file.write(key)
        print(f'Secret Key generated in the location: {file_location}')