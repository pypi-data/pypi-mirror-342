# Esewa Profanity Detection Package

This package is mainly used for detecting profanity for different languages specially, with Devnagari and Latin script.

Overall package is structured in the following way:

```
Esewa-Profanity-Detection
├── key_generator: Generates key for encrypting files.
├── encryptor : Encrypts the plain text file to encrypted files.
├── files : Directory for storing key, encrypted files and unicode files.
└── profanity_detector: Library for detecting profanity.
```

## 1. Key generator

Key generator uses Fernet and generates key. The generated key is stored in `files > keys`.

Basically one key is generated and overriden. i.e. `secret.key`.

But the immutable key `static_secret.key` is always placed.

Use the class `KeyGenerator` to instantiate and run method `generate()` from the package to generate unique secret key.


## 2. Encryptor

Encryptor enccrypts the plain text file given by the User and stores the data into `files > encoded_files`.

Two keys (`secret.key` and `static_secret.key`)are used for encrypting files. 

`static_secret.key` encrypts the predefined english and nepali bad words file.

`secret.key` encrypts the custom english and nepali bad words file.

Encrypted files will be in `.enc` format files.

Use the class `PreDefinedEncryptor` to instantiate and run method `encrypt(english_file, nepali_file)` in order to encrypt predefined english and nepali file. 

![Custom encryptor](/src/custom_encryption.png)

Use the class `CustomEncryptor` to instantiate and run method `encrypt(is_itreable=True, english_itreable, nepali_itreable)` in order to encrypt custom english and nepali list or set.

Use the class `CustomEncryptor` to instantiate and run method `encrypt(is_itreable=False, english_file, nepali_file)` in order to encrypt custom english and nepali file.


## 3. Profanity Detector

Profanity detector takes up text from the user. If the profanity is detected, then system provides user the prompt of profanity.

The encrypted file is now, decrypted with the key generated. For custom badwords, decryption is done with `secret.key` whereas for predefined badwords decryption is done with `static_secret.key`.


Use the class `ProfanityChecker` to instantiate and run method `detect_profanity(text)` with the `text` to detect profanity.

![Profanity Detection](/src/profanity_detection.png)

### Demo

```bash
$ pip install -r requirements.txt

$ python main.py
```

