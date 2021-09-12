import time
import sys
import random
from os.path import isfile
from cryptography.fernet import Fernet
from loguru import logger

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
    obj = time.strptime("13 9 2021", "%d %m %Y") #Set your date here
    nd = (obj.tm_mday, obj.tm_mon, obj.tm_year)
    now = (loc.tm_mday, loc.tm_mon, loc.tm_year)
    lst = list(zip(now, nd))
    if lst[2][0]>lst[2][1]:
       logger.debug("YEAR is valid, decrypting!")
       return True
    else:
        if lst[1][0]>lst[1][1]:
            logger.debug("MOUNTH is valid, decrypting!")
            return True
        elif lst[1][0] == lst[1][1] and lst[0][0]>=lst[0][1]:
            logger.debug("Mounth of day is valid, decrypting!")
            return True
        else:
            logger.error("Invalid date!")
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

except IndexError as IE:
    print("Give me a key-file!")

if timeChecker() == True:
    key = load_key(keyfile)
    decrypt(key)
else:
    print("Wrong date kiddy...")
