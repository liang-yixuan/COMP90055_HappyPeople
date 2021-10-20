from ssd_2 import SSD
from flask import Flask, request, send_from_directory, jsonify
import os
from PIL import Image
import cv2
import numpy as np
import json

model_path_emo = r'model_data/emotion_1.pth'
model_path_age = r'model_data/age_1.pth'
model_path_race = r'model_data/race_1.pth'
model_path_gender = r'model_data/gender_1.pth'

labels_emo = 'model_data/emo.txt'
labels_age = 'model_data/age.txt'
lavels_race = 'model_data/race.txt'
labels_gender = 'model_data/gender.txt'

json_dir = 'json/'
img_dir = 'img/'

ssd_emo = SSD(model_path=model_path_emo, classes_path=labels_emo)
ssd_age = SSD(model_path=model_path_age, classes_path=labels_age)
ssd_race = SSD(model_path=model_path_race, classes_path=lavels_race)
ssd_gender = SSD(model_path=model_path_gender, classes_path=labels_gender)


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
Threshold = 0.8

@app.route("/", methods=['POST'])
def predict():
    for i in os.listdir(img_dir):
        file_path = os.path.join(img_dir, i)
        os.remove(file_path)

    img = request.files.get("file")
    image = Image.open(img)
    imgName = img.filename
    img.save(os.path.join(img_dir, imgName))
    image_emo = ssd_emo.detect_image(image)
    image_age = ssd_age.detect_image(image)
    image_race = ssd_race.detect_image(image)
    image_gender = ssd_gender.detect_image(image)
    print(image_gender[1])
    obj_list = []


    if len(image_gender[1]) <=0:
        resultName = imgName[:imgName.find(".")] + "_det.jpg"
        RGB_img = image.convert('RGB')
        RGB_img.save(os.path.join(img_dir, resultName))
        with open(os.path.join(json_dir, imgName[:imgName.find(".")] + ".json"), 'w', encoding="utf-8") as f:
            # obj_json = json.dumps(obj_list)
            json.dump(obj_list, f)
        return send_from_directory(img_dir, os.path.join(img_dir, resultName), resultName)

    for i in zip(image_gender[0], image_gender[1], image_gender[2]):
        y1, x1, y2, x2 = np.array(i[0]).tolist()
        score = i[1]
        cls = i[2]
        new_obj = {"object":len(obj_list) + 1, "x1": x1, "y1": y1, "x2": x2, "y2": y2, "gender_class_label": cls}
        obj_list.append(new_obj)

    for i in zip(image_age[0], image_age[1], image_age[2]):
        y1, x1, y2, x2 = np.array(i[0]).tolist()
        score = i[1]
        cls = i[2]
        for obj in obj_list:
            if compute_iou([obj["y1"], obj["x1"], obj["y2"], obj["x2"]], [y1, x1, y2, x2]) >= Threshold:
                obj["age_class_label"] = cls

    for i in zip(image_emo[0], image_emo[1], image_emo[2]):
        y1, x1, y2, x2 = np.array(i[0]).tolist()
        score = i[1]
        cls = i[2]
        for obj in obj_list:
            if compute_iou([obj["y1"], obj["x1"], obj["y2"], obj["x2"]], [y1, x1, y2, x2]) >= Threshold:
                obj["emo_class_label"] = cls

    for i in zip(image_race[0], image_race[1], image_race[2]):
        y1, x1, y2, x2 = np.array(i[0]).tolist()
        score = i[1]
        cls = i[2]
        for obj in obj_list:
            if compute_iou([obj["y1"], obj["x1"], obj["y2"], obj["x2"]], [y1, x1, y2, x2]) >= Threshold:
                obj["ethnicity_class_label"] = cls

    resultName = imgName[:imgName.find(".")] + "_det.jpg"
    # im = Image.open(os.path.join(img_dir, imgName))
    RGB_img = drawBoundingBoxes(np.array(image), obj_list)
    RGB_img = Image.fromarray(RGB_img)
    RGB_img = RGB_img.convert('RGB')
    RGB_img.save(os.path.join(img_dir, resultName))

    with open(os.path.join(json_dir, imgName[:imgName.find(".")] + ".json"), 'w', encoding="utf-8") as f:
        # obj_json = json.dumps(obj_list)
        # obj_list = str(obj_list)
        json.dump(obj_list, f)

    return send_from_directory(img_dir, os.path.join(img_dir, resultName), resultName)


@app.route("/detections", methods=['POST'])
def return_json():
    json_name = request.data.decode("utf-8")
    with open(os.path.join(json_dir, json_name + ".json"), 'r', encoding="utf-8") as f:
        obj_list = json.load(f)

    for i in os.listdir(json_dir):
        file_path = os.path.join(json_dir, i)
        os.remove(file_path)
    return jsonify({"response": obj_list})


def compute_iou(rec1, rec2):
    """
    computing IoU
    :param rec1: (y0, x0, y1, x1), which reflects
            (top, left, bottom, right)
    :param rec2: (y0, x0, y1, x1)
    :return: scala value of IoU
    """
    # computing area of each rectangles
    S_rec1 = (rec1[2] - rec1[0]) * (rec1[3] - rec1[1])
    S_rec2 = (rec2[2] - rec2[0]) * (rec2[3] - rec2[1])

    # computing the sum_area
    sum_area = S_rec1 + S_rec2

    # find the each edge of intersect rectangle
    left_line = max(rec1[1], rec2[1])
    right_line = min(rec1[3], rec2[3])
    top_line = max(rec1[0], rec2[0])
    bottom_line = min(rec1[2], rec2[2])

    # judge if there is an intersect
    if left_line >= right_line or top_line >= bottom_line:
        return 0
    else:
        intersect = (right_line - left_line) * (bottom_line - top_line)
        return (intersect / (sum_area - intersect)) * 1.0


def drawBoundingBoxes(imageData, inferenceResults):
    """Draw bounding boxes on an image.
    imageData: image data in numpy array format
    imageOutputPath: output image file path
    inferenceResults: inference results array off object (l,t,w,h)
    colorMap: Bounding box color candidates, list of RGB tuples.
    """
    for res in inferenceResults:
        x1 = int(res['x1'])
        y1 = int(res['y1'])
        x2 = int(res['x2'])
        y2 = int(res['y2'])

        label = 'person_' + str(res['object'])
        color = (255, 199, 50)
        imgHeight, imgWidth, _ = imageData.shape
        thick = int((imgHeight + imgWidth) // 300)
        cv2.rectangle(imageData, (x1, y1), (x2, y2), color, thick)
        cv2.putText(imageData, label, (x1, y1 - 5), 2, 1e-3 * (imgHeight + imgWidth), color, thick // 2)

    return imageData


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
