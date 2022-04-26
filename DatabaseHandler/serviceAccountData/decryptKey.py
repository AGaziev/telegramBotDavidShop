from cryptocode import decrypt
import os

def getKey():
    with open('encryptedKey','r') as key:
        s = key.read()
        return decrypt(s,os.getenv('SAPasswordToEncrypt'))