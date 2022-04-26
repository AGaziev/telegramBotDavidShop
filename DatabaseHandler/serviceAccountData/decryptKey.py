from cryptocode import decrypt
import os

def getKey():
    with open('encryptedKey','r') as key:
        return decrypt(key.read(),os.getenv('SAPasswordToEncrypt'))