# AES_Time_Crypt
Python scripts which encrypt and decrypt files.
Could be used for NNN(*No Nut November*), some coders on freelanse (*not be tricked by customer*) and etc.

##Example\n
###Creating key\n
`python3 encrypt.py text.txt`
**Did you have a key-file? (y/n):** `n`
**Making a new file named key.key**

###Encrypting with generated key
`python3 encrypt.py text.txt key.key`
**Did you have a key-file? (y/n):** `y`
(file was encrypted)

###Decrypting file with key
`python3 decrypt.py text.txt key.key`
(file was decrypted)

###Time-Check function
`python3 decrypt.py text.txt key.key`
**Wrong date kiddy...**
You could change date in **decrypt.py** *timeChecker()* function ;)

*In future commits it`ll be normally obfuscated*
