import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from sklearn import metrics
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

df = pd.read_csv('labels_segmented_test.csv')
df = df.iloc[7:, :]

numpy_arr = df.to_numpy()
#print(numpy_arr[:][:])

img_train = []
img_train_labels = []
img_test = []
img_test_labels = []
ctr = 0

#Cleaning
#Son 1371 test
letterCountInWords = [0] * 41371
letterCountInPhotos = [0] * 41371
uncleanWords = []
cleanWords = []

for i in range(len(numpy_arr)):
    indexStr = numpy_arr[i][0]
    end = indexStr.index('_', 5)
    index = int(indexStr[5:end])
    letterCountInWords[index] += 1

for i in range(41371):
    if i < 10:
        noStr = '000' + str(i)
    elif i < 100:
        noStr = '00' + str(i)
    elif i < 1000:
        noStr = '0' + str(i)
    else:
        noStr = str(i)
    tryingNo = 0
    exists = True
    while(exists):
        path = "/Users/Gunes Ustunalp/Downloads/Compressed/test/TEST_" + noStr + "_segmented_" + str(tryingNo) + ".jpg"
        img = glob.glob(path)
        if img:
            tryingNo += 1
        else:
            letterCountInPhotos[i] = tryingNo
            exists = False
            #print(str(i) + " finished with " + str(tryingNo))


for i in range(len(letterCountInWords)):
    #print(str(i) + " - " + str(letterCountInWords[i]) + " - " + str(letterCountInPhotos[i]))
    if letterCountInWords[i] == letterCountInPhotos[i]:
        cleanWords.append(i)
    else:
        uncleanWords.append(i)

print("Clean Word Count: " + str(len(cleanWords)))
print("Unclean Word Count: " + str(len(uncleanWords)))

for i in range(len(numpy_arr)):
    indexStr = numpy_arr[i][0]
    end = indexStr.index('_', 5)
    index = int(indexStr[5:end])
    if index in cleanWords:
        path = "/Users/Gunes Ustunalp/Downloads/Compressed/test/" + numpy_arr[i][0]
        img = glob.glob(path)
        if img:
            colimg = Image.open(img[0])
            resized_Image = colimg.resize((32, 32))
            pix_val = list(resized_Image.getdata())
            pix_val_flat = [x for sets in pix_val for x in sets]
            if index <= 40000:
                img_train.append(pix_val_flat)
                img_train_labels.append(numpy_arr[i][1])
            else:
                img_test.append(pix_val_flat)
                img_test_labels.append(numpy_arr[i][1])
        else:
            print("There is a problem with the word cleaning process")
            ctr = ctr + 1
# ###
print("CTR is " + str(ctr))

print("The size of training set is " + str(len(img_train)))
print("The size of test set is " + str(len(img_test)))

GNB_classifier = GaussianNB()
GNB_classifier.fit(img_train, img_train_labels)

predicted = GNB_classifier.predict(img_test)
accuracy = accuracy_score(predicted, img_test_labels)

print("Accuracy: " + str(accuracy))