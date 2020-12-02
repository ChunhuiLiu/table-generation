import json
import os
import shutil
from tqdm import tqdm
import cv2
import time
import multiprocessing
from pprint import pprint


with open('files', 'r', encoding='utf-8') as fr_files:
    file_list = json.load(fr_files)

file_list = [[item[0].split('.')[0] + '_0.txt', item[1].split('.')[0] + '_0.txt'] for item in file_list]
picture_list = [item[0].split('.')[0] + '_0_ori.jpg' for item in file_list]
# if 'table2_274_0.txt' not in file_list:
#     print('table2_274_0.txt不在里面')
file_dir = os.path.join(os.getcwd(), 'cooked')
file_list = [[os.path.join(file_dir, item[0]), os.path.join(file_dir, item[1])] for item in file_list]
results = []
results_dir = 'table'

if not os.path.exists(results_dir):
    os.mkdir(results_dir)
else:
    shutil.rmtree(results_dir)
    os.mkdir(results_dir)


def worker(file1, file2):
    table1, table2 = [], []
    picture = file1.replace('.txt', '_ori.jpg')
    # print(picture)
    img = cv2.imread(picture)
    size_y = img.shape[0]
    size_x = img.shape[1]
    try:

        with open(file1, 'r', encoding='utf-8') as f1:
            while True:
                line = f1.readline()
                if not line:
                    break
                if line.startswith('##LTLine##'):
                    table1.append(list(map(int, line.split()[1:5])))

        with open(file2, 'r', encoding='utf-8') as f2:
            while True:
                line = f2.readline()
                if not line:
                    break
                if line.startswith('##LTLine##'):
                    table2.append(list(map(int, line.split()[1:5])))

        # 先合并一下
        table1_new = []
        map_table = {}
        for item in table1:
            # 横线
            if item[1] == item[3]:
                table1_new.append(item)
            # 竖线，x相同
            if item[0] == item[2]:
                if item[0] not in map_table:
                    map_table[item[0]] = [[item[1], item[3]]]
                else:
                    # 合并
                    flag = True
                    for i in range(len(map_table[item[0]])):
                        # 这里默认item这条线是要合并的线的后面连续位置的，其实数据是这样的表格中竖线的识别是从上到下一块一块的
                        if map_table[item[0]][i][1] >= item[1] - 5:
                            map_table[item[0]][i][1] = item[3]
                            flag = False
                            break
                    if flag:
                        map_table[item[0]].append([item[1], item[3]])
        for k in map_table:
            for v in map_table[k]:
                table1_new.append([k, v[0], k, v[1]])

        table2_new = []
        map_table = {}
        for item in table2:
            # 横线
            if item[1] == item[3]:
                table2_new.append(item)
            # 竖线，x相同
            if item[0] == item[2]:
                if item[0] not in map_table:
                    map_table[item[0]] = [[item[1], item[3]]]
                else:
                    # 合并
                    flag = True
                    for i in range(len(map_table[item[0]])):
                        if map_table[item[0]][i][1] >= item[1] - 5:
                            map_table[item[0]][i][1] = item[3]
                            flag = False
                            break
                    if flag:
                        map_table[item[0]].append([item[1], item[3]])
        for k in map_table:
            for v in map_table[k]:
                table2_new.append([k, v[0], k, v[1]])

        # pprint(table1_new)
        # pprint(table2_new)

        # table1, table2 resize
        def _resize_x(x):
            return int(x*size_x/1000)

        def _resize_y(y):
            return int(y*size_y/1000)
        table1_new = [[_resize_x(item[0]), _resize_y(item[1]), _resize_x(item[2]), _resize_y(item[3])] for item in table1_new]
        table2_new = [[_resize_x(item[0]), _resize_y(item[1]), _resize_x(item[2]), _resize_y(item[3])] for item in table2_new]

        def judge(table, item):
            for t in table:
                temp = sum([abs(x-y) for x, y in zip(t, item)])
                if temp <= 10:
                    return True
            return False

        result = []
        for item in table2_new:
            # 横线
            if item[1] == item[3]:
                if judge(table1_new, item):
                    result.append('##LTLine## VR '+' '.join(map(str, item)))
                else:
                    result.append('##LTLine## IR ' + ' '.join(map(str, item)))
            # 竖线
            if item[0] == item[2]:
                if judge(table1_new, item):
                    result.append('##LTLine## VC '+' '.join(map(str, item)))
                else:
                    result.append('##LTLine## IC ' + ' '.join(map(str, item)))

        # results.append(result)

        file = os.path.join(os.getcwd(), results_dir, os.path.basename(file1))
        with open(file, 'w', encoding='utf-8') as f:
            for line in result:
                f.write(line + '\n')

    except FileNotFoundError:
        print('{}文件没找到'.format(file1))


if __name__ == '__main__':
    pbar = tqdm(total=len(file_list))
    # pbar.set_description(' Flow ')
    update = lambda *x: pbar.update()

    pool = multiprocessing.Pool(processes=8)  # 8
    start = time.time()

    for file1, file2 in file_list:
        pool.apply_async(worker, (file1, file2), callback=update)

    pool.close()
    pool.join()
    end = time.time()
    print('程序执行时间：', end-start)

# 8
# 程序执行时间： 181.20193815231323
# 100%|█████████████████████████████████████████████████████████████████| 50000/50000 [03:01<00:00, 275.90it/s]

# 16
# 100%|████████████████████████████████████████████████████████████████▉| 49995/50000 [02:33<00:00, 329.58it/s]
# 程序执行时间： 153.5109190940857

# 24
# 程序执行时间： 147.33803153038025
# 100%|█████████████████████████████████████████████████████████████████| 50000/50000 [02:27<00:00, 339.28it/s]

# 32
# 程序执行时间： 147.84384751319885
# 100%|█████████████████████████████████████████████████████████████████| 50000/50000 [02:27<00:00, 338.10it/s]

# 40
# 程序执行时间： 148.08986949920654
# 100%|█████████████████████████████████████████████████████████████████| 50000/50000 [02:28<00:00, 337.52it/s]



