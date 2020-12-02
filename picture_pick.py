import json
import os
import shutil
from tqdm import tqdm
from pprint import pprint


"""
提取cooked文件夹中的原图
保存到picture文件夹中
"""

with open('files', 'r', encoding='utf-8') as fr_files:
    file_list = json.load(fr_files)

file_dir = os.path.join(os.getcwd(), 'cooked')
file_list = [os.path.join(file_dir, item[0].split('.')[0] + '_0_ori.jpg') for item in file_list]

result_dir = 'picture'

if not os.path.exists(result_dir):
    os.mkdir(result_dir)
else:
    shutil.rmtree(result_dir)
    os.mkdir(result_dir)

for file in tqdm(file_list):
    if os.path.exists(file):
        # print(file)
        shutil.copy(file, result_dir)
        # os.system('cp {} {}'.format(file, result_dir))
