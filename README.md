# AES_Time_Crypt
Python scripts which encrypt and decrypt files.<br/>
Could be used for NNN(*No Nut November*), some coders on freelanse (*not be tricked by customer*) and etc.<br/>

##Example<br/>
###Creating key<br/>
`python3 encrypt.py text.txt`<br/>
**Did you have a key-file? (y/n):** `n`<br/>
**Making a new file named key.key**<br/>

###Encrypting with generated key<br/>
`python3 encrypt.py text.txt key.key`<br/>
**Did you have a key-file? (y/n):** `y`<br/>
(file was encrypted)<br/>

###Decrypting file with key<br/>
`python3 decrypt.py text.txt key.key`<br/>
(file was decrypted)<br/>

###Time-Check function<br/>
`python3 decrypt.py text.txt key.key`<br/>
**Wrong date kiddy...**<br/>
You could change date in **decrypt.py** *timeChecker()* function ;)<br/>
*In future commits it`ll be normally obfuscated*
