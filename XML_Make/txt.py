import pandas as pd
import numpy as np
import os
import shutil
import traceback

os.getcwd()
os.chdir(r'C:\Users\CSY\Desktop\database\label\age\train')
path = r'C:\Users\CSY\Desktop\database\label\age\train'
outputPath = r'C:\Users\CSY\Desktop\database\label\age\test'

dataList = os.listdir(path)
print(os.listdir(path))

# coding=utf-8
import os
import shutil
import traceback


def move_file(src_path, dst_path, file):
    print('from : ', src_path)
    print('to : ', dst_path)

    try:
        f_src = os.path.join(src_path, file)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)
        f_dst = os.path.join(dst_path, file)
        shutil.move(f_src, f_dst)
    except Exception as e:
        print
        'move_file ERROR: ', e
        traceback.print_exc()



for i in dataList:
    if 'test' in i:
        move_file(path, outputPath, i)
