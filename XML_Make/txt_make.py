import os

os.getcwd()
os.chdir(r'C:\Users\CSY\Desktop\database\basic\Annotation\manual')
path = r'C:\Users\CSY\Desktop\database\basic\Annotation\manual'
outputPath = 'C:\\Users\\CSY\\Desktop\\database\\label\\age\\test\\'

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


for file in dataList:
    with open(file) as fr:
        name = file[:9]
        age_label = fr.readlines()[7]
        if '0' in age_label:
            age = '0-3'
        elif '1' in age_label:
            age = '4-19'
        elif '2' in age_label:
            age = '20-39'
        elif '3' in age_label:
            age = '40-69'
        elif '4' in age_label:
            age = '70+'

        dirFileList = os.listdir(outputPath)
        for j in dirFileList:
            if name in j:
                f_dst = os.path.join(outputPath, j)
                with open(f_dst, 'r+') as f:
                    content = f.read()
                    f.seek(0, 0)
                    f.write(age + '\n' + content)







# # bound分隔写入
# for file in dataList:
#     f_dst = os.path.join(outputPath, file)
#     with open(f_dst, 'r+') as f:
#         for line in f.readlines():
#             temp = line.split()
#             f.seek(0)
#             f.truncate()
#             for i in temp[:-1]:
#                 f.write(i)
#                 f.write('\n')
#             f.write(temp[-1])


# 批量重命名
# import os
#
# #获取该目录下所有文件，存入列表中
# f = os.listdir(outputPath)
#
# n=0
# for i in f:
#
#     #设置旧文件名（就是路径+文件名）
#     oldname = outputPath + f[n]
#
#     #设置新文件名
#     newname = outputPath+ f[n][0:11] +'.txt'
#
#     #用os模块中的rename方法对文件改名
#     os.rename(oldname, newname)
#     print(oldname,'======>',newname)
#
#     n+=1






