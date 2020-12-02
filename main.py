import os
import json
import shutil
from table import Table
from tqdm import tqdm

result_dir = 'result'
generation_num = 50000

sentence_length_range = [100, 150]  # 生成的句子长度的范围
table_row_range = [2, 6]  # 表格行的范围
table_column_range = [3, 6]  # 表格列的范围
table_title_range = [10, 15]  # 表格标题长度范围

if not os.path.exists(result_dir):
    os.mkdir(result_dir)
else:
    shutil.rmtree(result_dir)
    os.mkdir(result_dir)

table = Table(sentence_length_range, table_row_range, table_column_range, table_title_range)
name_table = []
for _ in tqdm(range(generation_num)):
    template_origin, template_full_border = table.run_double()
    origin_file_name = 'table1_{}.tex'.format(_)
    full_border_file_name = 'table2_{}.tex'.format(_)
    name_table.append([origin_file_name, full_border_file_name])
    with open(os.path.join(result_dir, origin_file_name), 'w', encoding='utf-8') as fw_1, open(os.path.join(result_dir, full_border_file_name), 'w', encoding='utf-8') as fw_2:
        fw_1.write(template_origin)
        fw_2.write(template_full_border)

with open('files', 'w', encoding='utf-8') as f:
    json.dump(name_table, f, ensure_ascii=False, indent=4)


