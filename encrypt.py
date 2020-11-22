from cryptography.fernet import Fernet
import sys
from os.path import isfile

#TODO if argv!=null => don`t ask about file

try:
    filename = sys.argv[1]
    if not isfile(filename):
        print("It`s not a file babe")
        exit()
except IndexError as IE:
    print("Give a name of file pls\nPrint usage ...")


def write_key():
    key = Fernet.generate_key()
    with open("key.key", 'wb') as key_file:
        key_file.write(key)

def load_key(keyfile):
    return open(f'{keyfile}', 'rb').read()

def encrypt(key):
    f = Fernet(key)
    try:
        file = open(filename, 'rb')
        file_data = file.read()
        encrypted_data = f.encrypt(file_data)
    except Exception as e:
        print("Something wrong in encryption")
    finally:
        file.close()

    try:
        file = open(filename, 'wb')
        file.write(encrypted_data)
    except Exception as e:
        print("Failed to rewrite  file")
    finally:
        file.close()


#print("BE CAREFUL WITH 'key.key'! THIS FILE IS KEY FROM YOUR FILES\nSAVE IT IF YOU DIDN`T WANT TO LOSE YOUR FILES")
answr = input("Did you have a key-file? (y/n): ")
if answr == 'n' or answr == 'N':
    print('Making a new file named key.key')
    write_key()
elif answr == 'y' or 'Y':
    try:
        keyfile = sys.argv[2]
        key = load_key(keyfile)
        encrypt(key)
    except IndexError as IE:
        print("Where is a key-file? A?M?")
