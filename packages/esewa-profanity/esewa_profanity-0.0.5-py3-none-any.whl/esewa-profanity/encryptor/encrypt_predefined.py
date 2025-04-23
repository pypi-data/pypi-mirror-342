from cryptography.fernet import Fernet
import os
# from pathlib import Path

class PreDefinedEncryptor:
    def __init__(self):
        cwd = os.getcwd()
        self.key_location = os.path.join(cwd, 'files','keys', 'static_secret.key')
        # encrypted_english_text = os.path.join(cwd, 'files', 'encoded_files','')
        self.english_encrypted_file = os.path.join(cwd, 'files', 'encoded_files', 'english_badwords.enc')
        self.nepali_encrypted_file = os.path.join(cwd, 'files', 'encoded_files', 'nepali_badwords.enc')

    def read_key(self)->Fernet:
        """Reads the previously generated key.

        Returns:
            Fernet: Fernet object with read key.
        """        
        key_location = self.key_location
        with open(key_location, 'rb') as key_file:
            key = key_file.read()
        fernet = Fernet(key)
        return fernet
    
    def read_plaintext_file(self, file_location:str)->bytes:
        """Reads the bad words plain text file from location

        Args:
            file_location (str): File location of the plaintext file.

        Returns:
            bytes: badwords in the form of encoded form of utf-8
        """        
        with open(file_location, 'r', encoding='utf-8') as file:
            bad_words = file.read().encode()
        return bad_words
    
    def encrypt_to_file(self, plaintext_location:str, target_file_location:str)->None:
        """Encrypts the single plain text file to binary encoded files

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
    
    def encrypt(self, english_plaintext_file:str, nepali_plaintext_file:str)->None:
        """Encrypts the english and nepali latin script files to encoded enc file.

        Args:
            english_plaintext_file (str): Location of encoded english plaintext file
            nepali_plaintext_file (str): Location of encoded nepali latin script plain text file
        """        
        english_encrypted_file = self.english_encrypted_file
        nepali_encrypted_file = self.nepali_encrypted_file
        self.encrypt_to_file( plaintext_location=english_plaintext_file ,target_file_location= english_encrypted_file)
        self.encrypt_to_file(plaintext_location=nepali_plaintext_file, target_file_location=nepali_encrypted_file)
