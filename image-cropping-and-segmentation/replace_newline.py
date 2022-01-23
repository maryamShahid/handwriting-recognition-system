import os
import glob
import re

folders = ['train', 'validation', 'test']
os.chdir('dataset')

i = 1
for folder in folders:
    j = 1
    arr = glob.glob( folder + "/coords/*.cropinfo")
    for filename in arr:
        #print(filename)
        enc = 'iso-8859-15'
        f = open(filename, "r", encoding=enc)
        if os.stat(filename).st_size == 0:
            continue

        content = f.read()
        f.close()

        content = content.replace('""', '"')
        f = open(filename, "w")
        f.write(content)
        f.close()
        j += 1

        print("folder %d file %d" % (i, j))
    i += 1
