import os

os.getcwd()
os.chdir('C:\\Users\\CSY\\Desktop\\database\\label\\emotion\\train\\')
path = r'C:\Users\CSY\Desktop\database\basic\Annotation\manual'
outputPath = 'C:\\Users\\CSY\\Desktop\\database\\label\\emotion\\train\\'

dataList = os.listdir(outputPath)

for file in dataList:
    with open(file, 'a+') as f:
        f.write('\n')  # 加\n换行显示
