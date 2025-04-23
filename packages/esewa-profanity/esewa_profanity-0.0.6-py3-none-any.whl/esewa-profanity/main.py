from key_generator import KeyGenerator
from encryptor import CustomEncryptor, PreDefinedEncryptor
from profanity_detector import ProfanityChecker
# import os


if __name__ == '__main__':
    # key_generator = KeyGenerator()
    # key_generator.generate()
    # cwd = os.getcwd()
    # english_file = os.path.join(cwd, 'predefined_english_badwords.txt')
    # nepali_file = os.path.join(cwd, 'predefined_nepali_badwords.txt')
    # predefined_encryptor = PreDefinedEncryptor()
    # predefined_encryptor.encrypt(english_plaintext_file=english_file, nepali_plaintext_file=nepali_file)
    # custom_nepali_file = os.path.join(cwd, 'custom_nepali_badwords.txt')
    # custom_english_file = os.path.join(cwd, 'custom_english_badwords.txt')
    # custom_encryptor = CustomEncryptor()
    # custom_encryptor.encrypt(is_itreable_passed=True, english_itreable=['thong'], nepali_itreable=['madhisey'])
    profanity_checker = ProfanityChecker()
    profanity_checker.detect_profanity('Hello fvck Ganj* with thong, madhisey')
    