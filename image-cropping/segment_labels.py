import os
import csv
import glob

def segment_csv(inpt, out):
    csv_dict = {}
    with open(inpt, mode='r') as inp:
        reader = csv.reader(inp)
        csv_dict = {rows[0]:rows[1] for rows in reader}
    result_dict = {}
    for i in csv_dict:
        #print(i)
        base = i.split(".")[0] + "_segmented_"
        #print(base)
        word = csv_dict[i].replace(" ", "")
        for j in range(len(word)):
            fn = base + str(j) + ".jpg"
            print(fn)
            result_dict[fn] = word[j]

    with open(out, 'w') as f:
        for key in result_dict.keys():
            f.write("%s,%s\n"%(key,result_dict[key]))

segment_csv("dataset/labels_train.csv", "dataset/labels_segmented_train.csv")
segment_csv("dataset/labels_validation.csv", "dataset/labels_segmented_validation.csv")
segment_csv("dataset/labels_test.csv", "dataset/labels_segmented_test.csv")
