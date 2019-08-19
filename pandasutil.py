import pandas
import os


# 写入数据
def write_csv_data(headers, dates, file_path):
    # 已经存在时追加数据
    if os.path.exists(file_path):
        df = pandas.DataFrame(dates,columns=None)
        df.to_csv(file_path, index=False, encoding="utf_8_sig",header=False, mode="a")
    else:
        # 第一次写入，需要表头信息
        df = pandas.DataFrame(dates, columns=headers)
        df.to_csv(file_path, index=False, encoding="utf_8_sig")


# 读取数据
def read_csv_data(file_path):
    try:
        datas = pandas.read_csv(file_path, encoding="utf_8_sig")
    except FileNotFoundError:
        datas = []
    return datas




