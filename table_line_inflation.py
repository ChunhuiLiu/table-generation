import os
import shutil
from tqdm import tqdm


table_dir = 'table'
outline_dir = 'table_line'
cwd = os.path.abspath(os.path.dirname(__file__))
tables = [os.path.join(cwd, table_dir, file) for file in os.listdir(table_dir)]

if not os.path.exists(outline_dir):
    os.mkdir(outline_dir)
else:
    shutil.rmtree(outline_dir)
    os.mkdir(outline_dir)


for table in tqdm(tables):
    with open(table, 'r', encoding='utf-8') as f_table:
        lines = f_table.read().splitlines()
    ans = []
    for line in lines:
        temp = []
        line = line.split()
        label = line[0:2]
        bbox = line[2:]
        temp.extend(label)
        if bbox[0] == bbox[2]:
            temp.extend([str(int(bbox[0])-10), bbox[1], str(int(bbox[2])+10), bbox[3]])
        elif bbox[1] == bbox[3]:
            temp.extend([bbox[0], str(int(bbox[1])-5), bbox[2], str(int(bbox[3])+5)])
        else:
            print('bbox不是一条线，file:', table)
        ans.append(temp[:])


    # rows = [t.split()[2:] for t in tables if t.split()[1][1] == 'R']
    # for i in range(1, len(rows)):
    #     if int(rows[i][1]) - int(rows[i-1][1]) <= 80:
    #         end_line = rows[i]
    #     else:
    #         outlines.append([begin_line[0], begin_line[1], end_line[2], end_line[3]])
    #         begin_line = rows[i]
    #         end_line = []
    # if end_line:
    #     outlines.append([begin_line[0], begin_line[1], end_line[2], end_line[3]])

    with open(os.path.join(outline_dir, os.path.basename(table)), 'w', encoding='utf-8') as f_outline:
        for line in ans:
            f_outline.write(' '.join(line) + '\n')
