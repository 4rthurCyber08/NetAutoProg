import os
from cryptography.fernet import Fernet

#file list container
victim_file = []

for file in os.listdir():
    if file == "encrypt.py" or file == "thekey.key" or file == "decrypt.py":
        continue
    if os.path.isfile(file):
        victim_file.append(file)

print(victim_file)

with open("the_key.key", "rb") as thekey:
    secret_key = thekey.read()

for file in victim_file:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    decrypt_contents = Fernet(secret_key).decrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(decrypt_contents)