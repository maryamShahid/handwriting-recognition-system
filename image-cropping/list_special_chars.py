import os
import glob



folders = ['train', 'validation', 'test']

special_chars = ""

os.chdir('dataset')
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ\n "

i = 1

print("From cropinfos:")
for folder in folders:
    arr = glob.glob( folder + "/coords/*.cropinfo")
    j = 0
    for filename in arr:
        #print(filename)
        enc = 'iso-8859-15'
        f = open(filename, "r", encoding=enc)
        if os.stat(filename).st_size == 0:
            continue

        for char in f.read().split('"')[1].upper():
            if char not in alphabet and char not in special_chars:
                special_chars += char

        j += 1
        #print(special_chars)
        #print("file", j, "in folder", i)
        f.close()

    i += 1

print(special_chars)


print("From labels:")
special_chars = ""
arr = glob.glob("*.csv")
for filename in arr:
    f = open(filename, "r", encoding=enc)
    for line in f:
        for char in line.split(',')[1].upper():
            if char not in alphabet and char not in special_chars:
                special_chars += char
    f.close()

print(special_chars)
