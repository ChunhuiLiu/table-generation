### setup
- 生成表格pdf和对应的全框线pdf  
    `python main.py`
- latex 转 pdf
    + 安装TeX Live
    + 确保xelatex命令可用  
        `$ xelatex`  
        `This is XeTeX, Version 3.14159265-2.6-0.99998 (TeX Live 2017/Debian) (preloaded format=xelatex)
         restricted \write18 enabled.
        **`
    + 生成pdf
        - `cd pdf`
        - `python latex2pdf.py`
- 调用生成DocBank的源码提取pdf中框线信息  
    `python pdf_process.py --data_dir pdf --output_dir cooked`
- 后处理，合并短的表格框线为一根长的线  
    `python post_process.py`
- 提取表格外轮廓
    `python outline_extract.py`
- 获取表格线对应的较大矩形的bbox
    `python table_line_inflation.py`

### 文件夹说明
- `result`: 保存latex文件
- `pdf`: 保存pdf文件
- `cooked`: 保存从pdf中提取的文字框线图片等信息
- `table`: 保存合并后的表格框线信息
- `outline`: 保存表格外轮廓bounding box
- `picture`: 保存从cooked文件夹中提取的原图
    
    
