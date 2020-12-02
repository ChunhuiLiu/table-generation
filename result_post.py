import os


"""
删除result中非tex文件
"""


file_list = os.listdir('result')
file_path_list = [os.path.join(os.getcwd(), 'result', file) for file in file_list]

# 清空已有
for file in file_path_list:
    if not file.endswith('.tex'):
        os.remove(file)
