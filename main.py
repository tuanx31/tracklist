import os
from mutagen.mp3 import MP3
import datetime
from tkinter import *
from tkinter import filedialog
import cv2


t = Tk()
duration = 0  # bien thoi gian global
lap = 1  # bien lap
# hàm xử lí thời gian


def xu_li_file(file_txt):
    with open(file_txt, "rb+") as f:
        f.seek(-9, os.SEEK_END)  # Đưa con trỏ đến vị trí cần xóa
        f.truncate()  # Xóa các byte kế tiếp vị trí đó
        f.close()


def last_char(file_txt):
    global last_nine_chars
    with open(file_txt, "r") as f:
        last_nine_chars = file_txt[-9:]


def time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return (hours, minutes, int(seconds))

# hàm get path file


def open_file():
    path = filedialog.askdirectory()
    return path

# get path file txt


def filetxt(path):
    file_name = 'AAAAAAA.txt'
    file_dic = os.path.join(path, file_name)
    file_name = file_dic.encode('utf-8')
    print(file_name.decode('utf-8'))
    if file_name:
        path_var.set(file_name.decode('utf-8'))
    return file_name.decode('utf-8')


def file_goc(file_txt):
    f = open(file_txt, 'w', encoding="utf-8")
    f.write("Tracklist:\n")
    f.close()


def khoi_tao_file(file_txt):
    global duration
    (hours, minutes, seconds) = time(duration)
    delta = datetime.timedelta(
        hours=hours, minutes=minutes, seconds=(seconds))
    f = open(file_txt, 'a', encoding="utf-8")
    f.write(str(delta)+" ")
    f.close()


def leng(file, file_txt, path):
    global duration

    for t, dirs, files in os.walk(os.path.abspath(path)):
        if file.endswith(".mp3"):
            audio = MP3(os.path.join(t, file))
            duration = duration + (audio.info.length)
            (hours, minutes, seconds) = time(duration)
            delta = datetime.timedelta(
                hours=hours, minutes=minutes, seconds=(seconds))
            f = open(file_txt, 'a', encoding="utf-8")
            print(delta)

            # f.write(name_file+"\n",)
            f.write(str(delta)+" ")
        if file.endswith(".mp4"):
            filename = os.path.join(t, file)
            cap = cv2.VideoCapture(filename)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            duration += frame_count / fps
            (hours, minutes, seconds) = time(duration)
            delta = datetime.timedelta(
                hours=hours, minutes=minutes, seconds=(seconds))
            f = open(file_txt, 'a', encoding="utf-8")
            print(delta)
            f.write(str(delta)+" ")


def name_file(file, file_txt, path):
    global duration
    for t, dirs, files in os.walk(os.path.abspath(path)):
        if file.endswith(".mp3"):
            namefile = os.path.basename(file)
            name_filee = namefile.encode('utf-8').decode('utf-8')
            name_file = os.path.splitext(name_filee)[0]
            print(name_file)
            f = open(file_txt, 'a+', encoding="utf-8")
            f.write(name_file+"\n",)
            f.close()
        if file.endswith(".mp4"):
            namefile = os.path.basename(file)
            name_filee = namefile.encode('utf-8').decode('utf-8')
            name_file = os.path.splitext(name_filee)[0]
            print(name_file)
            f = open(file_txt, 'a+', encoding="utf-8")
            f.write(name_file+"\n",)
            f.close()


def details(path, file_txt):

    for t, dirs, files in os.walk(os.path.abspath(path)):
        for file in files:
            name_file(file, file_txt, path)
            leng(file, file_txt, path)


def o_file():

    path = path_var.get()
    if path:
        with open(path, "r", encoding="utf-8") as file:
            contents = file.read()
            text_box.delete("1.0", END)
            text_box.insert(END, contents)


def total_duration():
    global duration
    (hours, minutes, seconds) = time(duration)
    delta = datetime.timedelta(
        hours=hours, minutes=minutes, seconds=(seconds))
    return delta


def ghi_total_file(file_txt):
    delta = total_duration()
    f = open(file_txt, 'a', encoding="utf-8")
    f.write(str(delta))
    f.close()


def loop(file_txt, path):
    khoi_tao_file(file_txt)
    details(path, file_txt)
    xu_li_file(file_txt)
    last_char(file_txt)


def main():
    global duration
    global lap
    path = open_file()
    file_txt = filetxt(path)
    file_goc(file_txt)
    for i in range(lap):
        loop(file_txt, path)
    ghi_total_file(file_txt)
    duration = 0
    lap = 1


def lap_2():
    global lap
    lap = 2
    lap_2.configure(bg='#ff0000')


def lap_3():
    global lap
    lap = 3
    lap_3.configure(bg='#ff9d00')


def lap_4():
    global lap
    lap = 4
    lap_4.configure(bg='yellow')


def lap_5():
    global lap
    lap = 5
    lap_5.configure(bg='#00ff1a')


def lap_6():
    global lap
    lap = 6
    lap_6.configure(bg='#00ddff')


def lap_7():
    global lap
    lap = 7
    lap_7.configure(bg='#4B0082')


def lap_8():
    global lap
    lap = 8
    lap_8.configure(bg='#c800ff')


def lap_9():
    global lap
    lap = 9
    lap_9.configure(bg='#c800ff')


def lap_10():
    global lap
    lap = 10
    lap_10.configure(bg='#ff0066')


label = Label(t, text="chọn số lần lặp")
label.pack(side="left")

lap_2 = Button(t, text="2", command=lap_2)
lap_2.pack(side="left")
lap_3 = Button(t, text="3", command=lap_3)
lap_3.pack(side="left")
lap_4 = Button(t, text="4", command=lap_4)
lap_4.pack(side="left")
lap_5 = Button(t, text="5", command=lap_5)
lap_5.pack(side="left")
lap_6 = Button(t, text="6", command=lap_6)
lap_6.pack(side="left")
lap_7 = Button(t, text="7", command=lap_7)
lap_7.pack(side="left")
lap_8 = Button(t, text="8", command=lap_8)
lap_8.pack(side="left")
lap_9 = Button(t, text="9", command=lap_9)
lap_9.pack(side="left")
lap_10 = Button(t, text="10", command=lap_10)
lap_10.pack(side="left")

main = Button(t, text="chọn foder lưu nhạc", command=main)
main.pack()

open_file_button = Button(t, text="mở file txt vừa run", command=o_file)
open_file_button.pack()

path_var = StringVar()
path_label = Label(t, textvariable=path_var)
path_label.pack()

text_box = Text(t, height=30, width=50)
text_box.pack()

t.mainloop()
