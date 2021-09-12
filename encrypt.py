from cryptography.fernet import Fernet
import sys
from os.path import isfile

#TODO if argv!=null => don`t ask about file

try:
    filename = sys.argv[1]
    if not isfile(filename):
        print("It`s not a file!")
        exit()
except IndexError as IE:
    print("Give me file as next argument!")


def write_key(keyfilename:str):
    key = Fernet.generate_key()
    with open(f"{keyfilename}.key", 'wb') as key_file:
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
def main():
    if len(sys.argv) == 1:
        print("Check a README.MD before usage...")
        return
    elif len(sys.argv) < 3:
        print("It seems what you didn't have a 'key' file\nLets generate it!")
        key_file_name = input("Give a name for key: ")
        write_key(key_file_name)
        keyfile = key_file_name+'.key'
        print("\n"+keyfile+' was created successfully!')
    elif len(sys.argv) == 3:
        keyfile = sys.argv[2]
        print(keyfile+" using as a key!")
    try:
        key = load_key(keyfile)
        encrypt(key)
    except IndexError as IE:
        print("Where is a key-file? A?M?")
    finally:
        print(f"File {sys.argv[1]} was encrypted!")

main()
