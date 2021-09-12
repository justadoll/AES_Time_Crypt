# AES_Time_Crypt

>Python scripts which encrypt and decrypt files.
Could be used for NNN(*No Nut November*), some coders on freelance (*not be tricked by customer*) etc.

Requirements

```bash
pip install cryptography loguru
```

***

## Example

### Creating key

```bash
$ python3 encrypt.py text.txt
It seems what you didn't have a 'key' file
Lets generate it!
Give a name for key: key
key.key was created successfully!
File creds.txt was encrypted!
```

***

### Encrypting with generated key

```bash
$ python3 encrypt.py another_creds.txt key.key

key.key using as a key!
File creds.txt was encrypted!
```

### Decrypting file with key

```bash
$ python3 decrypt.py creds.txt key.key
```

If date is correct in ```decrypt.py``` file will be decrypted
Check next module to get more information

***

### Time-Check function

```bash
$ python3 decrypt.py creds.txt key.key
2021-09-12 13:37:00.41 | ERROR    | __main__:timeChecker:39 - Invalid date!
Wrong date kiddy...
```
When I was trying to decrypt the date was 12.09.2021, but in timeChecker on 24 line was set on 13.09.2021

You could change date in **decrypt.py** *timeChecker()* function
Format is {day 1-31} {month 1-12} {year 202*}

In future commits, it will normally obfuscate to compile
