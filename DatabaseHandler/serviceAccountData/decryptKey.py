from cryptocode import decrypt
import os

def getKey():
    with open('serviceAccountData/encryptedKey.txt','r') as key:
        s = key.read()
        return decrypt(s,os.getenv('SAPasswordToEncrypt'))