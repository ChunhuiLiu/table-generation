import cv2
import os
import json

"""
展示cooked文件夹中源pdf和提取出的表格框线
"""

with open('files', 'r', encoding='utf-8') as fr_files:
    file_list = json.load(fr_files)

file_dir = os.path.join(os.getcwd(), 'cooked')
picture_list = [os.path.join(file_dir, item[0].split('.')[0] + '_0_ori.jpg') for item in file_list]
line_info_list = [os.path.join(os.getcwd(), 'table_line', item[0].split('.')[0] + '_0.txt') for item in file_list]

for picture, line_file in zip(picture_list, line_info_list):
    # print(picture)
    # print(os.path.exists(picture))
    img = cv2.imread(picture)
    if img is None:
        continue
    # img = cv2.resize(img, (1000, 1000))
    # size_x, size_y = img.shape
    # print(img.shape)
    # cv2.imshow(',', img)
    # cv2.waitKey(0)
    with open(line_file, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    lines = [line.split()[2:] for line in lines]
    for bbox in lines:
        cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0))

    print(picture)
    print(line_file)
    print(img.shape)

    cv2.imshow(os.path.basename(picture), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
