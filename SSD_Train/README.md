## SSD Implementation in Pytorch

## Required Environment
```console
pip install -r requirements.txt
```

## Download Weights Document
The weights of ssd_weights.pth and backbone required for training can be downloaded online<br>

## Training steps
### Train your own data set
1. Data set preparation<br>
**This project uses VOC format for training, you need to make a good data set before training, **<br>
Before training, put the label file in the Annotation under the VOC2007 folder under the VOCdevkit folder.<br>
Before training, place the picture files in JPEGImages in the VOC2007 folder under the VOCdevkit folder.<br>

2. Data set processing
After finishing the placement of the data set, we need to use voc_annotation.py to obtain 2007_train.txt and 2007_val.txt for training.<br>
Modify the parameters in voc_annotation.py. <br>
In the first training, only classes_path can be modified, and classes_path is used to point to the txt corresponding to the detection category.<br>
When training your own data set, you can create a cls_classes.txt, which contains the categories you need to distinguish.<br>
The content of the model_data/cls_classes.txt file is:<br>
```python
cat
dog
...
```<br>
Modify the classes_path in voc_annotation.py to correspond to cls_classes.txt, and run voc_annotation.py.

3. Start network training<br>
**There are many training parameters, all of which are in train.py. You can read the comments carefully after downloading the library. The most important part is still the classes_path in train.py. **<br>
**classes_path is used to point to the txt corresponding to the detection category, this txt is the same as the txt in voc_annotation.py! The data set for training yourself must be modified! **<br>
After modifying the classes_path, you can run train.py to start training. After training multiple epochs, the weights will be generated in the logs folder.<br>

4. Training result prediction<br>
Two files are needed to predict the training results, namely ssd.py and predict.py. Modify model_path and classes_path in ssd.py.<br>
**model_path points to the trained weight file, which is in the logs folder.<br>
The classes_path points to the txt corresponding to the detection category. **<br>
After the modification is completed, you can run predict.py for detection. After running, enter the image path to detect.<br>
<br>

## Reference
https://github.com/pierluigiferrari/ssd_keras  
https://github.com/kuhung/SSD_keras  
