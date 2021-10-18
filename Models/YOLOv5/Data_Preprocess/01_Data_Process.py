'''
    File name:
    Author: Yixuan Liang
    Python Version: 3.8
'''
"""
Transform the label format from three different resources to a single 
to 4 separate label files stored in the corresponding folder

Resource:
The bounding box information is contained in the "boundingbox" folder
The labels for age, ethnicity and gender are contained in the "manual" folder
The emotion label is contained in the "EmoLabel" folder

Destination:
txt file containing 1 label and 4 normalised coordinates of the bounding box in the label_xxx folder
e.g., 
2 0.50658 0.34096 0.36541 0.31567 -- in the labels_age folder
4 0.50658 0.34096 0.36541 0.31567 -- in the labels_emotion folder
2 0.50658 0.34096 0.36541 0.31567 -- in the labels_ethnicity folder
1 0.50658 0.34096 0.36541 0.31567 -- in the labels_gender folder
"""

import PIL
import os

def main(set, output_class):
    # print("Current working directory: {0}".format(os.getcwd()))
    num_test = 3068
    num_train = 12271

    def convert_label(bounding_box, label):
        bounding_box = list(map(float, bounding_box))

        bbx_width = round((bounding_box[2] - bounding_box[0]) / width, 5)
        bbx_height = round((bounding_box[3] - bounding_box[1]) / height, 5)
        x_center = round(((bounding_box[2] + bounding_box[0]) / 2) / width, 5)
        y_center = round(((bounding_box[3] + bounding_box[1]) / 2) / height, 5)
        new_label = list(map(str, [label, x_center, y_center, bbx_width, bbx_height]))

        new_label = ' '.join(new_label)
        return new_label


    if set == "train":
        samples = num_train
    else:
        samples = num_test

    def emo_dictionary(emo_filename):
        dictionary = {}
        file = open(emo_filename)
        for line in file:
            key, value = line.split()
            dictionary[key] = int(value) - 1  # yolo required zero-index
        # values = dictionary.values()
        # from collections import Counter
        # count = Counter(values)
        # print("extracted emotions:", count)
        return dictionary

    emo_filename = "EmoLabel/list_patition_label.txt"
    emotions = emo_dictionary(emo_filename)

    for image_id in range(1, samples+1):

        if set == "train":
            img_folder = "train/"
            img_head = "train_"
            image_ids = str(f'{image_id:05}')
        else:
            img_folder = "val/"
            img_head = "test_"
            image_ids = str(f'{image_id:04}')

        image_name = img_head + image_ids + ".jpg"
        image_filename = "data/images/" + img_folder + image_name
        label_outut_filename = "data/labels_"+output_class+"/" + img_folder + img_head + image_ids + ".txt"
        bbx_filename = "boundingbox/" + img_head + image_ids + "_boundingbox.txt"
        label_filename = "manual/" + img_head + image_ids + "_manu_attri.txt"

        image = PIL.Image.open(image_filename)
        width, height = image.size

        bbx_file = open(bbx_filename, "r")
        bounding_box = bbx_file.read().split(" ")[:-1]

        label_file = open(label_filename, "r")
        labels = label_file.read().split("\n")[5:8]
        gender = labels[0]
        ethnicity = labels[1]
        age = labels[2]

        emotion = emotions[image_name]

        if output_class == "gender":
            new_label = convert_label(bounding_box, gender)
        elif output_class == "ethnicity":
            new_label = convert_label(bounding_box, ethnicity)
        elif output_class == "age":
            new_label = convert_label(bounding_box, age)
        elif output_class == "emotion":
            new_label = convert_label(bounding_box, emotion)

        # write output label
        f = open(label_outut_filename, "w")
        f.write(new_label)
        f.close()


###################
sets = ["train","test"]
output_classes = ["gender", "ethnicity", "age", "emotion"]
for set in sets:
    for output_class in output_classes:
        main(set, output_class)
