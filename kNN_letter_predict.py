#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 18:29:03 2021

@author: turanmertduran
"""
import cv2
import glob
from PIL import Image
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
df = pd.read_csv('/Users/turanmertduran/Desktop/segmented/labels_segmented_train.csv')
df = df.iloc[6: , :]

numpy_arr = df.to_numpy()
print(numpy_arr[0][0])
cv_img_train = []
cv_img_train_labels = []
ctr = 0
for i in range(0,200000):
    path = "/Users/turanmertduran/Desktop/segmented/train/" + numpy_arr[i][0]
    fileName = numpy_arr[i][0].split("segmented")
    img = glob.glob(path)
    if img:
        #print(i)
        colimg = Image.open(img[0])
        resized_image = colimg.resize((32,32))
        pix_val = list(resized_image.getdata())
        pix_val_flat = [x for sets in pix_val for x in sets]
        cv_img_train.append(pix_val_flat)
        cv_img_train_labels.append(numpy_arr[i][1])
    else:
        print(i)


dft = pd.read_csv('/Users/turanmertduran/Desktop/segmented/labels_segmented_test.csv')
dft = dft.iloc[8: , :]

#if glob.glob("E:\\Logs\\Filename.*"):

numpy_arrt = dft.to_numpy()
print(numpy_arrt[0][0])
cv_img_test = []
cv_img_test_labels = []
ctr = 0
#for i in range(0, 10000):
for i in range(0,20000):
    path = "/Users/turanmertduran/Desktop/segmented/test/" + numpy_arrt[i][0]
    #extension = numpy_arr[i][0]
    #print(path)
    img = glob.glob(path)
    if img:
        #print(i)
        colimg = Image.open(img[0])
        resized_image = colimg.resize((32,32))
        pix_val = list(resized_image.getdata())
        pix_val_flat = [x for sets in pix_val for x in sets]
        cv_img_test.append(pix_val_flat)
        cv_img_test_labels.append(numpy_arrt[i][1])
    else:
        print(i)

neighten = KNeighborsClassifier(n_neighbors = 10, p = 2)
neighten.fit(cv_img_train, cv_img_train_labels)
accuracy=neighten.score(cv_img_test[0:9000],cv_img_test_labels[0:9000])
print("accuracy: ", accuracy)
