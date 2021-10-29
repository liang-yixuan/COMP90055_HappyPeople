import colorsys
import os
import time
import warnings

import numpy as np
import torch
import torch.backends.cudnn as cudnn
from PIL import Image, ImageDraw, ImageFont

from nets import ssd
from utils.box_utils import letterbox_image, ssd_correct_boxes

warnings.filterwarnings("ignore")

MEANS = (104, 117, 123)



class SSD(object):
    _defaults = {
        "input_shape"       : (300, 300, 3),
        "confidence"        : 0.5,
        "nms_iou"           : 0.45,
        "cuda"              : False,
        "backbone"          : "vgg",
        "letterbox_image"   : False,
    }

    @classmethod
    def get_defaults(cls, n):
        if n in cls._defaults:
            return cls._defaults[n]
        else:
            return "Unrecognized attribute name '" + n + "'"




    def __init__(self, model_path, classes_path, **kwargs):
        self.__dict__.update(self._defaults)
        self.model_path = model_path
        self.classes_path = classes_path
        self.class_names = self._get_class()
        self.generate()
        



    def _get_class(self):
        classes_path = os.path.expanduser(self.classes_path)
        with open(classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names
    



    def generate(self):



        self.num_classes = len(self.class_names) + 1




        model = ssd.get_ssd("test", self.num_classes, self.backbone, self.confidence, self.nms_iou)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model.load_state_dict(torch.load(self.model_path, map_location=device))
        self.net = model.eval()

        if self.cuda:
            self.net = torch.nn.DataParallel(self.net)
            cudnn.benchmark = True
            self.net = self.net.cuda()

        hsv_tuples = [(x / len(self.class_names), 1., 1.)
                      for x in range(len(self.class_names))]
        self.colors = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        self.colors = list(
            map(lambda x: (int(x[0] * 255), int(x[1] * 255), int(x[2] * 255)),
                self.colors))




    def detect_image(self, image):

        image = image.convert('RGB')

        image_shape = np.array(np.shape(image)[0:2])




        if self.letterbox_image:
            crop_img = np.array(letterbox_image(image, (self.input_shape[1],self.input_shape[0])))
        else:
            crop_img = image.resize((self.input_shape[1],self.input_shape[0]), Image.BICUBIC)

        photo = np.array(crop_img,dtype = np.float64)
        with torch.no_grad():



            photo = torch.from_numpy(np.expand_dims(np.transpose(photo - MEANS, (2, 0, 1)), 0)).type(torch.FloatTensor)
            if self.cuda:
                photo = photo.cuda()
                



            preds = self.net(photo)
        
            top_conf = []
            top_label = []
            top_bboxes = []



            for i in range(preds.size(1)):
                j = 0
                while preds[0, i, j, 0] >= self.confidence:




                    score = preds[0, i, j, 0]
                    label_name = self.class_names[i-1]



                    pt = (preds[0, i, j, 1:]).detach().numpy()
                    coords = [pt[0], pt[1], pt[2], pt[3]]
                    top_conf.append(float(score.float()))
                    top_label.append(label_name)
                    top_bboxes.append(coords)
                    j = j + 1


        if len(top_conf)<=0:
            return [], top_conf, 'No'

        top_conf = np.array(top_conf)
        top_label = np.array(top_label)
        top_bboxes = np.array(top_bboxes)
        top_xmin, top_ymin, top_xmax, top_ymax = np.expand_dims(top_bboxes[:,0], -1),np.expand_dims(top_bboxes[:,1], -1),np.expand_dims(top_bboxes[:,2], -1),np.expand_dims(top_bboxes[:,3], -1)




        if self.letterbox_image:
            boxes = ssd_correct_boxes(top_ymin, top_xmin, top_ymax, top_xmax, np.array([self.input_shape[0],self.input_shape[1]]),image_shape)
        else:
            top_xmin = top_xmin * image_shape[1]
            top_ymin = top_ymin * image_shape[0]
            top_xmax = top_xmax * image_shape[1]
            top_ymax = top_ymax * image_shape[0]
            boxes = np.concatenate([top_ymin,top_xmin,top_ymax,top_xmax], axis=-1)









































        return boxes, top_conf, top_label
