from .better_profanity.better_profanity import Profanity
from .script_detector import ScriptDetector
import os
from pathlib import Path
from cryptography.fernet import Fernet
from typing import Set

class ProfanityChecker:
    def __init__(self):
        cwd = os.getcwd()
        self.static_secret_key_file = os.path.join(cwd, 'files','keys','static_secret.key')
        self.key_file = os.path.join(cwd, 'files','keys','secret.key')
        self.encrypted_english_badwords_file = os.path.join(cwd, 'files','encoded_files','english_badwords.enc')
        self.encrypted_nepali_badwords_file = os.path.join(cwd, 'files', 'encoded_files', 'nepali_badwords.enc')
        self.encrypted_custom_english_badwords_file = os.path.join(cwd, 'files', 'encoded_files', 'custom_english_badwords.enc')
        self.encrypted_custom_nepali_badwords_file = os.path.join(cwd, 'files', 'encoded_files', 'custom_nepali_badwords.enc')
        self.json_file_location = os.path.join(cwd, 'files','json','unicode_script.json')
        profanity = self.add_predefined_profanity()
        self.profanity = self.update_profanity_wordlist(profanity)
        self.script_detector = ScriptDetector()
    
    def read_key(self, key_file:str)-> Fernet:
        """Reads the key and stores in Fernet object from the Key file

        Args:
            key_file (str): Stored Key file

        Returns:
            Fernet: Fernet object that has key.
        """        
        with open(key_file, 'rb') as file:
            key = file.read()
        fernet = Fernet(key)
        return fernet
    
    def read_bad_words(self, encrypted_file_location:str)-> bytes:
        """Reads the bad words from the file location

        Args:
            encrypted_file_location (str): Location of encrypted file

        Returns:
            bytes: Read bad words in binary format.
        """        
        with open(encrypted_file_location, 'rb') as enc_file:
            encrypted_data = enc_file.read()
        return encrypted_data
    
    def decrypt_data(self, key:Fernet, encrypted_data:bytes) -> str:
        """Decrypts the data from the binary encrypted data with the use of key

        Args:
            key (Fernet): Fernet object with generated key
            encrypted_data (bytes): Encrypted data with binary format.

        Raises:
            ValueError: If key does not decrypt the word file.

        Returns:
            str: If success, decrypted text is returned.
        """        
        try:
            decrypted_data = key.decrypt(encrypted_data).decode('utf-8').strip()
            return decrypted_data
        except Exception as e:
            raise ValueError('Failed to decrypt bad words file. Ensure the key is correct.') from e
            
    def load_badwords(self, key_file:str, encrypted_file:str)->Set:
        """Loads the badwords based on encrypted key file and encrypted badwords file

        Args:
            key_file (str): Key file locationgenerated from fernet
            encrypted_file (str): Encrypted badwords file location

        Returns:
            Set: Set of badwords loaded from the file.
        """        
        key = self.read_key(key_file=key_file)
        encrypted_data = self.read_bad_words(encrypted_file_location=encrypted_file)
        decrypted_data = self.decrypt_data(key=key, encrypted_data=encrypted_data)
        bad_words = set(line.strip().lower() for line in decrypted_data.splitlines() if line.strip())
        return bad_words

    def extend_badwords(self, badwords:Set)->Set:
        """Extends bad words with use of * in both start and end of bad word
        i.e. abc -> *abc*

        Args:
            badwords (Set): bad words which needs to be extended

        Returns:
            Set: Extended bad words.
        """        
        badwords = list(badwords)
        extended_bad_words = badwords + [f"*{word}*" for word in badwords]
        return set(extended_bad_words)

    def add_predefined_profanity(self)->Profanity:
        """Predefined profanity is added for both english and nepali romanized texts.

        Returns:
            Profanity: Profanity object that adds the predefined nepali and english censor words.
        """        
        encrypted_english_badwords_file = self.encrypted_english_badwords_file
        encrypted_nepali_badwords_file = self.encrypted_nepali_badwords_file
        static_key_file = self.static_secret_key_file
        english_bad_words = self.load_badwords(key_file=static_key_file, encrypted_file=encrypted_english_badwords_file)
        extended_english_bad_words = self.extend_badwords(english_bad_words)
        nepali_bad_words = self.load_badwords(key_file=static_key_file, encrypted_file=encrypted_nepali_badwords_file)
        extended_nepali_bad_words = self.extend_badwords(nepali_bad_words)
        extended_english_bad_words.update(extended_nepali_bad_words)
        profanity = Profanity(words = extended_english_bad_words)
        return profanity

    def update_profanity_wordlist(self, profanity:Profanity)->Profanity:
        """Updates the censor words with custom english and nepali words.

        Args:
            profanity (Profanity): Profanity object with predefined nepali and english censor words.

        Returns:
            Profanity: Profanity object with updated censor words of nepali and english censor words.
        """        
        key_file = self.key_file
        encrypted_custom_english_file = self.encrypted_custom_english_badwords_file
        encrypted_custom_nepali_file = self.encrypted_custom_nepali_badwords_file
        custom_english_badwords = self.load_badwords(key_file= key_file, encrypted_file= encrypted_custom_english_file)
        extended_custom_english_badwords = self.extend_badwords(custom_english_badwords)
        custom_nepali_badwords = self.load_badwords(key_file=key_file, encrypted_file=encrypted_custom_nepali_file)
        extended_custom_nepali_badwords = self.extend_badwords(custom_nepali_badwords)
        extended_custom_english_badwords.update(extended_custom_nepali_badwords)
        profanity.add_censor_words(extended_custom_english_badwords)
        return profanity
    
    def detect_profanity(self, text:str):
        """Detects profanity based on the text given
        Provides profanity detection prompt to the user when detected. 

        Args:
            text (str): User povided texts.
        """        
        json_file_location = self.json_file_location
        profanity = self.profanity
        bad_words = []
        words = text.split()
        script_text = self.script_detector.detect(file_location=json_file_location, text=words[0])
        if script_text == 'Latin':
            for word in words:
                word = word.lower()
                if profanity.contains_profanity(word):
                    bad_words.append(word)
            if bad_words:
                print("Detected content is inappropriate/offensive. Kindly rephrase your message.")
            else:
                print("Your message is appropriate.")
        else:
            print('Other script detected')      
