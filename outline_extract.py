import os
import shutil
from tqdm import tqdm

"""
表格轮廓线抽取
"""

table_dir = 'table'
outline_dir = 'outline'
cwd = os.path.abspath(os.path.dirname(__file__))
tables = [os.path.join(cwd, table_dir, file) for file in os.listdir(table_dir)]

if not os.path.exists(outline_dir):
    os.mkdir(outline_dir)
else:
    shutil.rmtree(outline_dir)
    os.mkdir(outline_dir)

for table in tqdm(tables):
    with open(table, 'r', encoding='utf-8') as f_table:
        tables = f_table.read().splitlines()
    rows = [t.split()[2:] for t in tables if t.split()[1][1] == 'R']
    begin_line = rows[0]
    end_line = []
    outlines = []
    for i in range(1, len(rows)):
        if int(rows[i][1]) - int(rows[i-1][1]) <= 80:
            end_line = rows[i]
        else:
            outlines.append([begin_line[0], begin_line[1], end_line[2], end_line[3]])
            begin_line = rows[i]
            end_line = []
    if end_line:
        outlines.append([begin_line[0], begin_line[1], end_line[2], end_line[3]])

    with open(os.path.join(outline_dir, os.path.basename(table)), 'w', encoding='utf-8') as f_outline:
        for outline in outlines:
            f_outline.write(' '.join(outline) + '\n')

