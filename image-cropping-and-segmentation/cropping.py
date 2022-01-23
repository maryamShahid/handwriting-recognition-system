from fuzzywuzzy import fuzz
import os
import glob
from PIL import Image
import csv
import cv2


SCORE_TRESHOLD = 50

def englishify(word):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ret = ""

    for letter in word:

        if letter == " ": ret.append('S')
    return ret

def crop_image(image_path, left, top, right, bottom):
    img = Image.open(image_path)
    return img.crop((left, top, right, bottom))

class G_Row:
    def __init__(self, word, left, top, right, bottom):
        self.word = word
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
    def __str__(self):
        return "%s %d %d %d %d"%(self.word, self.left, self.top, self.right, self.bottom)

def search_label(label, arr):
    #print(label)
    max_score = 0
    max_i = -1
    max_j = -1
    for i in range(len(arr)):
        for j in range(i, len(arr)):
            test_str = ""
            for k in range(i, j + 1):
                test_str += arr[k].word
            current_score = fuzz.ratio(test_str, label)
            #print(test_str, current_score)
            if current_score > max_score:
                max_score = current_score
                max_i = i
                max_j = j
    return [max_score, max_i, max_j]

def crop_by_info(image_path, label, cropinfo_path):
    label = label.upper()
    cropinfo = open(cropinfo_path, "r")

    left = -1
    top = -1
    right = -1
    bottom = -1
    arr = []

    bll = True

    for line in cropinfo:
        if bll:
            bll = False
            continue
        #print(line)
        word = line.split('"')[1].replace(" ", "").upper()
        #print(word)
        l = -1
        r = -1
        t = -1
        b = -1
        for c in line.split('"')[2].strip().split():
            cor = c[1:][:-1].split(",")
            if l == -1 or int(cor[0]) < l:
                l = int(cor[0])
            if r == -1 or int(cor[0]) > r:
                r = int(cor[0])
            if t == -1 or int(cor[1]) < t:
                t = int(cor[1])
            if b == -1 or int(cor[1]) > b:
                b = int(cor[1])

        if word == label:
            #print(l,r,t,b)
            return crop_image(image_path, l, t, r, b)
        arr.append(G_Row(word, l, t, r, b))

    scores = search_label(label, arr)

    max_score = scores[0]
    max_i = scores[1]
    max_j = scores[2]

    if max_score < SCORE_TRESHOLD:
        return -1

    for k in range(max_i, max_j+1):
        if left == -1 or arr[k].left < left :
            left = arr[k].left
        if right == -1 or arr[k].right > right:
            right = arr[k].right
        if top == -1 or arr[k].top < top :
            top = arr[k].top
        if bottom == -1 or arr[k].bottom > bottom:
            bottom = arr[k].bottom
    im = cv2.imread(image_path)
    h, w, c = im.shape

    if left < 0:
        left = 0
    if top < 0:
        top = 0
    if bottom > h:
        bottom = h
    if right > w:
        right = w
    return crop_image(image_path, left, top, right, bottom)

os.chdir("dataset")
count = 0
for i in ["train", "validation", "test"]:
    csvname = "labels_" + i + ".csv"
    csv_dict = {}

    with open(csvname, mode='r') as inp:
        reader = csv.reader(inp)
        csv_dict = {rows[0]:rows[1] for rows in reader}

    # print(csv_dict)
    os.chdir(i)
    #crop_by_info("TRAIN_244274.jpg", "EMPTY", "coords/TRAIN_244274.cropinfo").show()
    #break
    errorfile = open("../cropped/" + i + "/errored.txt", mode='w+')
    for j in sorted(glob.glob("*.jpg")):
        cropinfoname = "coords/" + j.split(".")[0] + ".cropinfo"
        label = csv_dict[j]
        #print(j, cropinfoname, label)
        try:
            res = crop_by_info(j, label, cropinfoname)
        except:
            print(j)
            count += 1
        if res == -1:
            errorfile.write(j + "\n")
            continue

        newfn = "../cropped/" + i + "/" + j.split(".")[0] + "_cropped.jpg"
        #print(newfn)
        #print(res)
        try:
            res.save(newfn)
        except:
            count += 1
            print(count)
    errorfile.close()
    os.chdir("..")
print(count)
