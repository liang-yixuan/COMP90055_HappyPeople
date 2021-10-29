import os

os.getcwd()
os.chdir(r'C:\Users\CSY\Desktop\database\basic\EmoLabel')
path = r'C:\Users\CSY\Desktop\database\basic\EmoLabel'
# outputPath = 'C:\\Users\\CSY\\Desktop\\database\\label\\emotion\\test\\'
outputPath = 'C:\\Users\\CSY\\Desktop\\database\\label\\test\\train\\'

dataList = os.listdir(path)
# print(os.listdir(path))



# for i in dataList:
#     if 'train' in i:
#         with open(i) as fr:
#             age = fr.readlines()[5]
#             f_dst = os.path.join(outputPath, i)
#             with open(f_dst, 'r+') as f:
#                 content = f.read()
#                 f.seek(0, 0)
#                 f.write(age + '\n' + content)


for line in open(dataList[0]):
    if 'train' in line:
        name = line[:11]
        emo_label = line[-2]
    elif 'test' in line:
        name = line[:9]
        emo_label = line[-2]

    if '1' in emo_label:
        emo = 'Surprise'
    elif '2' in emo_label:
        emo = 'Fear'
    elif '3' in emo_label:
        emo = 'Disgust'
    elif '4' in emo_label:
        emo = 'Happiness'
    elif '5' in emo_label:
        emo = 'Sadness'
    elif '6' in emo_label:
        emo = 'Anger'
    elif '7' in emo_label:
        emo = 'Neutral'

    dirFileList = os.listdir(outputPath)
    for j in dirFileList:
        if name in j:
            f_dst = os.path.join(outputPath, j)
            with open(f_dst, 'r+') as f:
                content = f.read()
                f.seek(0, 0)
                f.write(emo + '\n' + content)

