from cryptography.fernet import Fernet
import os
from typing import Union, Set, List
# from pathlib import Path

class CustomEncryptor:
    def __init__(self):
        cwd = os.getcwd()
        self.key_location = os.path.join(cwd, 'files','keys', 'secret.key')
        self.custom_english_encrypted_file = os.path.join(cwd, 'files', 'encoded_files', 'custom_english_badwords.enc')
        self.custom_nepali_encrypted_file = os.path.join(cwd, 'files', 'encoded_files', 'custom_nepali_badwords.enc')

    def read_key(self)->Fernet:
        """Reads the key from the specific key location

        Returns:
            Fernet: Fernet object with generated key
        """                 
        key_location = self.key_location
        with open(key_location, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        return fernet
    
    def read_plaintext_file(self, file_location:str)-> bytes:
        """Reads plain text file and returns byte encoded file

        Args:
            file_location (str): Directory location of plain text file.
        Returns:
            bytes: bad words encoded on byte format.
        """        
        with open(file_location, 'r', encoding='utf-8') as file:
            bad_words = file.read().encode()
        return bad_words
    
    def encrypt_to_file(self, plaintext_location:str, target_file_location:str)->None:
        """Encrypts the single custom plain text file to binary encoded files

        Args:
            plaintext_location (str): Location of the plain text file
            target_file_location (str): Location of encoded enc file
        """        
        fernet = self.read_key()
        bad_words = self.read_plaintext_file(file_location=plaintext_location)
        encrypted_bad_words = fernet.encrypt(bad_words)
        with open(target_file_location, 'wb') as  encrypted_file:
            encrypted_file.write(encrypted_bad_words)
        print(f'Encrypted bad words saved to : {target_file_location}')
    
    def encrypt_itreable(self, itreable_plaintext:List, target_file_location:str)->None:
        bad_words = '\n'.join(itreable_plaintext).encode()
        fernet = self.read_key()
        encrypted_bad_words = fernet.encrypt(bad_words)
        with open(target_file_location, 'wb') as encrypted_file:
            encrypted_file.write(encrypted_bad_words)
        print(f'Encrypted bad words saved to : {target_file_location}')

    
    def encrypt(self,is_itreable_passed:bool = True,english_itreable:Union[Set,List]=None, nepali_itreable:Union[Set,List]=None,
                english_plaintext_file:str=None, nepali_plaintext_file:str=None)->None:
        custom_english_encrypted_file = self.custom_english_encrypted_file
        custom_nepali_encrypted_file = self.custom_nepali_encrypted_file
        if is_itreable_passed:
            english_itreable = list(set(english_itreable))
            nepali_itreable = list(set(nepali_itreable))
            self.encrypt_itreable(itreable_plaintext=english_itreable, target_file_location=custom_english_encrypted_file)
            self.encrypt_itreable(itreable_plaintext=nepali_itreable, target_file_location=custom_nepali_encrypted_file)
        else:        
            self.encrypt_to_file( plaintext_location=english_plaintext_file ,target_file_location= custom_english_encrypted_file)
            self.encrypt_to_file(plaintext_location=nepali_plaintext_file, target_file_location=custom_nepali_encrypted_file)
