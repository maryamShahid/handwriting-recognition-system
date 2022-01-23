from PIL import Image
import os
import csv
import glob

def segment_image(image_path):
    img = Image.open(image_path)
    bw = img.convert('1')
    img.show()

    w,h = bw.size
    #print(w,h)
    image_area = False
    start = 0

    segmented_images = []

    for i in range(w):

        is_column_empty = True
        for j in range(h):
            pixel = bw.getpixel((i,j))
            if pixel == 0:
                is_column_empty = False


        if (is_column_empty or i == w-1) and image_area:
            cropped_bw = bw.crop((start,0,i,h))
            cropped = img.crop((start,0,i,h))

            td_start = -1
            td_end = -1
            cw, ch = cropped.size
            for j in range(ch):
                row_empty = True
                for k in range(cw):
                    pixel = cropped_bw.getpixel((k, j))
                    if pixel == 0:
                        row_empty = False
                if row_empty and td_start != -1 and td_end == -1 or j == ch - 1:
                    td_end = j
                    break
                if not row_empty and td_start == -1:
                    td_start = j
            # print(ch)
            # print(td_start, td_end)
            cropped = cropped.crop((0, td_start, cw, td_end))
            cropped_bw = cropped_bw.crop((0, td_start, 0, td_end))
            segmented_images.append(cropped)

            #cropped.resize([int(2 * s) for s in cropped.size]).show()
            image_area = False
        if not is_column_empty:
            if not image_area:
                start = i
            image_area = True
    return segmented_images



res = segment_image("dataset/cropped/train/TRAIN_00001_cropped.jpg")
#print(len(res))

exit()

os.chdir("dataset/cropped")
correct = 0
incorrect = 0
for i in ["train", "validation", "test"]:
    csvname = "../labels_" + i + ".csv"
    csv_dict = {}

    with open(csvname, mode='r') as inp:
        reader = csv.reader(inp)
        csv_dict = {rows[0]:rows[1] for rows in reader}

    # print(csv_dict)
    os.chdir(i)
    #crop_by_info("TRAIN_244274.jpg", "EMPTY", "coords/TRAIN_244274.cropinfo").show()
    #break
    count = 0
    for j in sorted(glob.glob("*.jpg")):
        print(count)
        label = csv_dict[j.replace("_cropped", "")]
        res = segment_image(j)
        #print(len(label), len(res))
        if len(label) == len(res):
            correct += 1
        else:
            incorrect += 1

        for k in range(len(res)):
            newfn = j.replace("_cropped", "").split(".")[0] + "_segmented_" + str(k) + ".jpg"
            #print(newfn)
            res[k].save("../../segmented/" + i + "/" + newfn )
        count += 1
    os.chdir("..")

print(correct * 100 / (correct + incorrect))
