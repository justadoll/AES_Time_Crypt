import time
import sys
from os.path import isfile
from cryptography.fernet import Fernet

def load_key(keyfile):
    return open(f'{keyfile}', 'rb').read()


def decrypt(key):
    f = Fernet(key)
    with open(filename, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(filename, 'wb') as file:
        file.write(decrypted_data)


### CHECKER FUNC ###
def timeChecker():
    loc = time.localtime()
    obj = time.strptime("1 12 2020", "%d %m %Y") #Set your date here
    nd = (obj.tm_mday, obj.tm_mon, obj.tm_year)
    now = (loc.tm_mday, loc.tm_mon, loc.tm_year)
    lst = list(zip(now, nd))
    tmp = 0
    for i in lst:
        if(i[0] >= i[1]):
            tmp += 1
        else:
            pass
    if tmp == 3:
        return True
    else:
        return False

#FILE 
try:
    filename = sys.argv[1]
    if not isfile(filename):
        print("It`s not a file babe")
        exit()
except IndexError as IE:
    print("print usage")

#KEY
try:
    keyfile = sys.argv[2]
    if not isfile(keyfile):
        print("It`s not a key babe")
        exit()
except IndexError as IE:
    print("Give me a key-file!")
    exit()

if timeChecker() == True:
    key = load_key(keyfile)
    decrypt(key)
else:
    print("Wrong date kiddy...")
