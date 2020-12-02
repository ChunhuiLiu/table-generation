import random
import numpy as np
from utils import sentence_generation
from utils import random_word


def table_paragraph_num():
    # 1表:2表:3表 = 6:3:1
    table_num_temp = random.randint(0, 9)
    if table_num_temp < 6:
        table_num = 1
    elif 6 <= table_num_temp < 9:
        table_num = 2
    else:
        table_num = 3
    paragraph_num = 3 - table_num
    return table_num, paragraph_num


class Table:
    def __init__(self, sentence_length_range, table_row_range, table_column_range, table_title_range):
        self.sentence_length_range = sentence_length_range
        self.table_row_range = table_row_range
        self.table_column_range = table_column_range
        self.table_title_range = table_title_range
        # self.paragraph_num = 2  # 默认两个段落
        # self.table_num = 1  # 默认一个表
        # self.table_num_range = [1, 3]
        self.table_type = ['full', 'no_left_right_border', 'three_line']
        # 这个cell宽度也要有一个range,不然固定长度深度模型容易学习这个长度来识别
        self.table_cell_width = np.linspace(1.0, 1.5, 6)  # 表格单元宽度，太宽会撑爆页面

        self.template_start = r"""\documentclass[UTF8]{ctexart}
%控制缩放
%\usepackage{graphicx}
\begin{document}"""
        self.template_end = r"""
\end{document}"""
        self.template_paragraph = r"""
\subparagraph{}
"""
        self.template_table = """
\\begin{{table}}[!htb]
\\centering
\\caption{{{}}}
\\label{{tab:resized}}
\\begin{{tabular}}{{{}}}
{}
\\end{{tabular}}
\\end{{table}}"""
        self.table_row_sep = ' \\hline\n'
        self.table_row_eos = r'\\'

    def run(self):
        """
        :return:符合XeLaTex格式的纯文本
        """

        table_num, paragraph_num = table_paragraph_num()

        # 构造段落
        paragraphs = []
        for i in range(paragraph_num):
            paragraphs.append(self.template_paragraph + sentence_generation(random.randint(*self.sentence_length_range)))

        # 构造表格
        tables = []
        for i in range(table_num):
            table, _ = self.table_generation(table_type=random.choice(self.table_type))
            tables.append(table)

        customized_content = paragraphs + tables
        random.shuffle(customized_content)

        template = self.template_start + ''.join(customized_content) + self.template_end
        return template

    def run_double(self):
        """
        :return: (str1, str2) str1: 符合XeLaTex格式的纯文本, str2: 对应的全边框表格
        """

        table_num, paragraph_num = table_paragraph_num()

        # 构造段落
        paragraphs_origin = []
        for i in range(paragraph_num):
            paragraphs_origin.append(self.template_paragraph + sentence_generation(random.randint(*self.sentence_length_range)))

        # 构造表格
        tables_origin = []
        tables_full_border = []
        for i in range(table_num):
            table1, table2 = self.table_generation(table_type=random.choice(self.table_type), double=True)
            tables_origin.append(table1)
            tables_full_border.append(table2)

        tables = list(zip(tables_origin, tables_full_border))
        paragraphs = list(zip(paragraphs_origin, paragraphs_origin))

        customized_content = paragraphs + tables
        random.shuffle(customized_content)
        template_origin_list, template_full_border_list = list(zip(*customized_content))

        template_origin = self.template_start + ''.join(template_origin_list) + self.template_end
        template_full_border = self.template_start + ''.join(template_full_border_list) + self.template_end
        return template_origin, template_full_border

    def table_generation(self, table_type='full', double=False):
        """
        :param table_type: {'full', 'no_left_right_border', 'three_line'}, optional, default: 'full'
        :param double: Boolean  if double is True, return original table and full-border table
        :return: str  the content of generated table
        """
        row = random.randint(*self.table_row_range)
        column = random.randint(*self.table_column_range)
        table_title = sentence_generation(random.randint(*self.table_title_range))
        # column_config = '|' + '|'.join(['p{{{}cm}}'.format(random.choice(self.table_cell_width)) for _ in range(column)]) + '|'  # '|p{2cm}|p{2cm}|'
        rows = ['&'.join([random_word() for i in range(column)]) + self.table_row_eos for _ in range(row)]

        table_full_border = ''
        if double:
            full_border_column_config = '|' + '|'.join(['c' for _ in range(column)]) + '|'
            full_border_rows_config = self.table_row_sep + ('\n' + self.table_row_sep).join(rows) + '\n' + self.table_row_sep
            table_full_border = self.template_table.format(table_title, full_border_column_config, full_border_rows_config)

        if table_type == 'full':
            column_config = '|' + '|'.join(['c' for _ in range(column)]) + '|'
            rows_config = self.table_row_sep + ('\n' + self.table_row_sep).join(rows) + '\n' + self.table_row_sep
        elif table_type == 'no_left_right_border':
            column_config = '|'.join(['c' for _ in range(column)])
            rows_config = self.table_row_sep + ('\n' + self.table_row_sep).join(rows) + '\n' + self.table_row_sep
        elif table_type == 'three_line':
            column_config = ''.join(['c' for _ in range(column)])
            rows = [rows[i] + '\n' + self.table_row_sep if i == 0 else rows[i] for i in range(len(rows))]
            rows_config = self.table_row_sep + '\n'.join(rows) + '\n' + self.table_row_sep
        else:
            raise Exception('无法识别的表格类型')

        table = self.template_table.format(table_title, column_config, rows_config)
        return table, table_full_border
