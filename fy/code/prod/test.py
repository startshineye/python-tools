import wave
import numpy as np
import os
from tkinter import *
from tkinter.filedialog import askopenfilename


# 获取文件路径函数
def select_file():
    file_path = askopenfilename()
    txt_path.set(file_path)


# 转换并生成wav文件函数
def convert():
    # 获取输入值
    fs = int(fs_entry.get())
    txt_file = txt_path.get()

    # 从txt文件路径中提取文件名
    txt_name = os.path.basename(txt_file)

    # 构造wav文件路径
    wav_file = txt_name.replace('txt', 'wav')

    # 打开txt文件并读取数据...

    # 生成wav文件
    wave_out = wave.open(wav_file, 'w')
    # ...

    # 提示信息
    info_label['text'] = '{} file generated!'.format(wav_file)


# GUI
root = Tk()
root.title('Sampling Rate Converter')

# 选择文件路径变量及按钮
txt_path = StringVar()
Button(root, text='Select txt File', command=select_file).grid(row=0, column=0)

# 采样率输入及标签
Label(root, text='Sampling Rate: ').grid(row=1, column=0)
fs_entry = Entry(root, width=10)
fs_entry.grid(row=1, column=1)

# 转换按钮
Button(root, text='Convert', command=convert).grid(row=2, column=0)

# 提示信息
info_label = Label(root)
info_label.grid(row=3, column=0)

root.mainloop()