from tkinter import *
from tkinter import filedialog
import tkinter as tk  # 使用Tkinter前需要先导入
import tkinter.messagebox  # 要使用messagebox先要导入模块
import os
import glob

NO_SUB = 0
INLINE_SUB = 1
INSIDE_SUB = 2
OUTSIDE_SUB = 3


class App:
    def __init__(self, master):
        # self.frame = Frame(master)
        # self.frame.grid()
        self.dir = StringVar()
        self.folder_name = StringVar()
        self.out_dir = StringVar()
        self.select_full_name = StringVar()
        self.fold_name_prefix = ""

        self.start_name = ""
        self.end_name = ""
        self.file_list = []
        self.fmt_file_list = []
        self.cur_video_format = ""
        self.cur_sub_format = ""
        self.last_dir = None
        self.filter_entry_list = []
        self.video_file_list = []
        self.sub_file_list = []


        lable_name = ["解析目录：", "文件夹名称:", "输出目录", "字幕封装类型:", "分辨率:", "字幕语音:"]
        x_p = 10
        y_p = 30
        cnt = 0
        for txt in lable_name:
            lable = Label(master, text=txt)
            lable.place(x=x_p, y=y_p)
            cnt += 1
            if cnt == 3:
                x_p = 800
                y_p = 30
                continue
            y_p += 50

        # dir input
        y_p = 30
        x_p = 80 + 10
        self.dir_line = Entry(master, textvariable=self.dir, width=80)
        self.dir_line.place(x=x_p, y=y_p)
        self.dir_line.bind('<Return>', self.dir_input)
        x_p += 575
        self.open_button = Button(master, text="open", command=self.open_file, width=11)
        self.open_button.place(x=x_p, y=y_p - 4)

        y_p += 50
        x_p = 80 + 10
        self.folder_name_line = Entry(master, textvariable=self.folder_name, width=80)
        self.folder_name_line.place(x=x_p, y=y_p)
        self.folder_name_line.bind('<Return>', self.name_change)
        self.folder_name_line.bind('<FocusOut>', self.name_change)
        x_p += 575
        self.rename_folder_button = Button(master, text="文件夹重命名", command=self.rename_folder, width=11)
        self.rename_folder_button.place(x=x_p, y=y_p - 4)

        y_p += 50
        x_p = 80 + 10
        self.out_dir_line = Entry(master, textvariable=self.out_dir, width=80, state="readonly")
        self.out_dir_line.place(x=x_p, y=y_p)

        x_p = 800 + 85
        y_p = 30
        self.sub_radio_list = []
        self.sub_type = StringVar()
        self.sub_select_text = ["无字幕", "内嵌", "内封", "外挂"]
        for txt in self.sub_select_text:
            radio = Radiobutton(master, text=txt, fg='blue', variable=self.sub_type, value=txt, command=self.sub_select)
            radio.place(x=x_p, y=y_p)
            self.sub_radio_list.append(radio)
            x_p += 80

        x_p = 800 + 85
        y_p += 50
        self.ration_radio_list = []
        self.rotion_type = StringVar()
        self.rotion_select_text = ["720P", "1080P", "未知"]
        for txt in self.rotion_select_text:
            radio = Radiobutton(master, text=txt, fg='blue', variable=self.rotion_type, value=txt, command=self.sub_select)
            radio.place(x=x_p, y=y_p)
            self.sub_radio_list.append(radio)
            x_p += 80

        x_p = 800 + 85
        y_p += 50
        self.language_box_list = []
        lang_CH = StringVar()
        lang_CH.set("")
        lang_Jp = StringVar()
        lang_Jp.set("")
        lang_split = IntVar()
        self.lag_select_text = [["中文", "ch", lang_CH, ""], ["日语", "Jp", lang_Jp, ""], ["字幕分离", 1, lang_split, -1]]
        for txt in self.lag_select_text:
            box = Checkbutton(master, text=txt[0], variable=txt[2], onvalue=txt[1], offvalue=txt[3], command=self.sub_select)
            box.place(x=x_p, y=y_p)
            x_p += 80
            self.language_box_list.append(box)

        x_p = 10
        y_p += 80
        y_tmp = y_p

        lable = Label(master, text="选中文件:")
        lable.place(x=x_p, y=y_p + 90)
        self.select_file_name = Entry(master, width=80, textvariable=self.select_full_name)
        self.select_file_name.place(x=x_p + 80, y=y_p + 90)

        x_p = 10
        y_p += 130
        x_tmp = x_p
        labe_list = [["视频列表", self.select_video_file, "open"], ["字幕列表", self.select_sub_file, "open"], ["重命名列表", self.rename_file, "write"]]
        for txt in labe_list:
            lable = Label(master, text=txt[0])
            lable.place(x=x_tmp, y=y_p)
            batton = Button(master, text=txt[2], command=txt[1], width=11)
            batton.place(x=x_tmp + 70, y=y_p-4)
            x_tmp += 460
        y_p += 30

        self.sbx = Scrollbar(root, orient=HORIZONTAL)
        self.sby = Scrollbar(root, orient=VERTICAL)
        self.sbx.place(x=x_p , y=y_p + 400, width=1350, height=16)
        self.sby.place(x=1360, y=y_p, width=16, height=300)

        self.video_show_list = Listbox(master, xscrollcommand=self.xxx_scroll, yscrollcommand=self.yyy_scroll, width=60, height=22)
        self.video_show_list.place(x=x_p, y=y_p)
        self.video_show_list.bind('<Double-Button-1>', self.file_select)
        x_p += 460
        self.sub_show_list = Listbox(master, xscrollcommand=self.xxx_scroll, yscrollcommand=self.yyy_scroll, width=60, height=22)
        self.sub_show_list.place(x=x_p, y=y_p)
        self.sub_show_list.bind('<Double-Button-1>', self.file_select)
        x_p += 460
        self.rename_show_list = Listbox(master, xscrollcommand=self.xxx_scroll, yscrollcommand=self.yyy_scroll, width=60, height=22)
        self.rename_show_list.place(x=x_p, y=y_p)
        self.rename_show_list.bind('<Double-Button-1>', self.file_select)

        self.sbx.config(command=self.xxx_set_view)
        self.sby.config(command=self.yyy_set_view)
        self.disable_all()

    def select_video_file(self):
        file_list = filedialog.askopenfiles(initialdir=self.last_dir)
        if len(file_list) == 0:
            return
        self.last_dir = ""
        self.video_file_list.clear()
        self.video_show_list.delete(0, END)
        for i in file_list:
            path = i.__getattribute__("name")
            name = os.path.split(path)[1]
            print(name)
            self.video_show_list.insert(END, name)
            self.video_file_list.append([os.path.splitext(name)[0], -1, os.path.split(path)[0], os.path.splitext(name)[1]])
            if self.last_dir == "":
                self.last_dir = os.path.split(path)[0]
        print(self.video_file_list)
        self.find_num_eig(self.video_file_list)


        if len(self.video_file_list) > 0:
            self.parser_same_eig()
        else:
            self.sub_file_list.delete(0, END)

    def select_sub_file(self):
        file_list = filedialog.askopenfiles(initialdir=self.last_dir)
        if len(file_list) == 0:
            return
        self.sub_file_list.clear()
        self.sub_show_list.delete(0, END)
        self.rename_show_list.delete(0, END)
        for i in file_list:
            path = i.__getattribute__("name")
            name = os.path.split(path)[1]
            print(name)
            self.sub_show_list.insert(END, name)
            self.sub_file_list.append([os.path.splitext(name)[0], -1, os.path.split(path)[0], os.path.splitext(name)[1]])
        print(self.sub_file_list)
        self.find_num_eig(self.sub_file_list)
        if len(self.video_file_list) > 0:
            self.parser_same_eig()
        else:
            self.rename_show_list.delete(0, END)

    def rename_file(self):
        t = tkinter.messagebox.askokcancel('文件重命名', "是否确定重命名列表中的文件??")  # 确定/取消，返回值true/false
        if not t:
            return
        self.sub_show_list.delete(0, END)
        self.rename_show_list.delete(0, END)
        for item in self.sub_file_list:
            print(item)
            if len(item) == 5:
                new = item[2] + "/" + item[4] + item[3]
                old = item[2] + "/" + item[0] + item[3]
                print(old)
                print(new)
                cnt = 0
                if os.path.isfile(new):
                    cnt += 1
                    new = item[2] + "/" + item[4] + (".(%d)" % cnt) + item[3]

                if old != new and os.path.isfile(old) and (not os.path.isfile(new)):
                    os.rename(old, new)

        self.sub_file_list.clear()

    def xxx_set_view(self, *args):
        self.video_show_list.xview(*args)
        self.sub_show_list.xview(*args)
        self.rename_show_list.xview(*args)

    def yyy_set_view(self, *args):
        print(*args)
        self.video_show_list.yview(*args)
        self.sub_show_list.yview(*args)
        self.rename_show_list.yview(*args)

    def xxx_scroll(self, a, b):
        self.sbx.set(a, b)
        self.video_show_list.xview_moveto(a)
        self.sub_show_list.xview_moveto(a)
        self.rename_show_list.xview_moveto(a)

    def yyy_scroll(self, a, b):
        self.sby.set(a, b)
        self.video_show_list.yview_moveto(a)
        self.sub_show_list.yview_moveto(a)
        self.rename_show_list.yview_moveto(a)

    def name_change(self, evt):
        self.sub_select()

    def dir_input(self, evt):
        print(self.dir.get())
        if not os.path.isdir(self.dir.get()):
            print("no such dir")
            tkinter.messagebox.showerror(title='Error', message='无效的路径')
            # self.disable_all()
            return
        else:
            self.prser_dir()

    def is_num(self, str):
        if len(str) == 0:
            return False
        if str.startswith("."):
            return False
        for c in str:
            if c not in "0123456789" and c != '.':
                return False
        return True

    def find_num_eig(self, list):
        print("find")
        print(list)
        same_str = list[0][0]
        print(same_str)
        find_none = 0
        for item in list:
            name = item[0]
            s = 0
            e = 0
            while e <= len(same_str):
                str = same_str[0:e]
                if not name.startswith(str):
                    if e > 0:
                        same_str = same_str[0:e-1]
                    else:
                        find_none = 1
                    break
                e += 1
            if find_none == 1:
                break
        print(same_str)

        same_len = len(same_str)
        for item in list:
            name = item[0]
            s = same_len
            while s <= len(name) - 1:
                str = name[s:s+1]
                if self.is_num(str):
                    break
                else:
                    s += 1
            e = s + 1
            while e <= len(name):
                str = name[s:e]
                if not self.is_num(str):
                    print(str[0:-1])
                    item[1] = float(str[0:-1])
                    break
                else:
                    e += 1
                    if e > len(name):
                        print(str)
                        item[1] = float(str)

        print(list)

    def parser_same_eig(self):
        rename_file_list = []
        for sub in self.sub_file_list:
            eig = sub[1]
            rename = ""
            for video in self.video_file_list:
                if eig == video[1]:
                    rename += video[0]
                    end = os.path.splitext(sub[0])[1]
                    print(end)
                    cnt = 0
                    tmp = rename
                    while (tmp + self.cur_sub_format) in rename_file_list:
                        cnt += 1
                        tmp = rename + (".(%d)" % cnt)
                    rename = tmp

                    rename += self.cur_sub_format
                    rename_file_list.append(rename)
                    print(rename)
                    sub.append(rename)
                    break
            if rename == "":
                self.rename_show_list.insert(END, "")
                continue
            self.rename_show_list.insert(END, rename + sub[3])

    def file_select(self, evt):
        tu = self.video_show_list.curselection()
        full_name = ""
        print(tu)
        if tu.__len__() > 0:
            self.select_full_name.set("")
            idx = self.video_show_list.curselection()[0]
            full_name = self.video_show_list.get(idx)
        else:
            tu = self.sub_show_list.curselection()
            print(tu)
            if tu.__len__() > 0:
                idx = self.sub_show_list.curselection()[0]
                full_name = self.sub_show_list.get(idx)
            else:
                tu = self.rename_show_list.curselection()
                print(tu )
                if tu.__len__() > 0:
                    idx = self.rename_show_list.curselection()[0]
                    full_name = self.rename_show_list.get(idx)
                else:
                    return
        print(full_name)
        self.select_full_name.set(os.path.splitext(full_name)[0])

    def sub_select(self):
        print(self.rotion_type.get())
        if self.rotion_type.get() == "unknown" or self.rotion_type.get() == "未知":
            self.fold_name_prefix = ""
        else:
            self.fold_name_prefix = self.rotion_type.get()

        if self.sub_type.get() == self.sub_select_text[0] or self.sub_type.get() == "unknown":
            for box in self.language_box_list:
                box['state'] = DISABLED
                box.deselect()
        else:
            self.language_box_list[0]['state'] = ACTIVE
            self.language_box_list[1]['state'] = ACTIVE
        if self.sub_type.get() != "unknown":
            self.fold_name_prefix += "[" + self.sub_type.get() + "]"

        if self.lag_select_text[0][2].get() != "" and self.lag_select_text[1][2].get() != "" and self.sub_type.get() != self.sub_select_text[1]:
            self.language_box_list[2]['state'] = ACTIVE
        else:
            self.language_box_list[2]['state'] = DISABLED
            self.language_box_list[2].deselect()

        if self.lag_select_text[2][2].get() == 1:
            if self.lag_select_text[0][2].get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.lag_select_text[0][2].get() + "]"
            if self.lag_select_text[1][2].get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.lag_select_text[1][2].get() + "]"
        else:
            if self.lag_select_text[0][2].get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.lag_select_text[0][2].get()
                if self.lag_select_text[1][2].get() != "":
                    self.fold_name_prefix = self.fold_name_prefix + "&&" + self.lag_select_text[1][2].get()
                self.fold_name_prefix = self.fold_name_prefix + "]"
            else:
                if self.lag_select_text[1][2].get() != "":
                    self.fold_name_prefix = self.fold_name_prefix + "[" + self.lag_select_text[1][2].get() + "]"

        print(self.fold_name_prefix)
        self.out_dir.set(os.path.dirname(self.dir.get()) + "/" + self.folder_name.get() + self.fold_name_prefix)

    def open_file(self):
        dir_path = filedialog.askdirectory(initialdir=self.last_dir)
        print(dir_path)
        if len(dir_path) > 0:
            self.dir.set(dir_path)
            self.prser_dir()
        else:
            print("no dir select")
            if self.dir.get() == "":
                self.disable_all()

    def prser_dir(self):
        self.disable_all()
        for radio in self.sub_radio_list:
            radio['state'] = ACTIVE
            # radio.deselect()

        for radio in self.ration_radio_list:
            radio['state'] = ACTIVE
            # radio.deselect()

        self.rename_folder_button['state'] = ACTIVE
        self.folder_name.set(os.path.basename(self.dir.get()))
        self.out_dir.set(os.path.dirname(self.dir.get()) + "/" + self.folder_name.get() + self.fold_name_prefix)
        self.last_dir = self.dir.get()
        return

    def disable_all(self):

        self.sub_type.set("unknown")
        for radio in self.sub_radio_list:
            radio['state'] = DISABLED
            # radio.deselect()

        self.rotion_type.set("unknown")
        for radio in self.ration_radio_list:
            radio['state'] = DISABLED
            # radio.deselect()

        for box in self.language_box_list:
            box['state'] = DISABLED
            box.deselect()

        self.rename_folder_button['state'] = DISABLED

        # self.out_dir_line.delete(0, END)
        # self.folder_name_line.delete(0, END)
        self.video_show_list.delete(0, END)
        self.sub_show_list.delete(0, END)
        self.rename_show_list.delete(0, END)

        self.file_list.clear()
        self.select_full_name.set("")
        self.cur_video_format = ""
        self.cur_sub_format = ""
        for entry in self.filter_entry_list:
            entry.delete(0, END)

    def rename_folder(self):
        print(self.dir.get())
        print(self.out_dir.get())

        if self.dir.get() == self.out_dir.get():
            tkinter.messagebox.showerror(title='Error', message='文件名相同')
            return

        if os.path.isdir(self.out_dir.get()):
            tkinter.messagebox.showerror(title='Error', message='输出文件夹已经存在')
            return

        str = self.dir.get() + " >>> " + self.out_dir.get() + "???"
        t = tkinter.messagebox.askokcancel('文件夹重命名', str)  # 确定/取消，返回值true/false
        print(t)
        if t:
            os.rename(self.dir.get(), self.out_dir.get())
            self.dir.set(self.out_dir.get())
            self.last_dir = self.out_dir.get()
            self.prser_dir()

if __name__ == '__main__':
    root = Tk()
    root.tk.eval('package require Tix')  # 引入升级包，这样才能使用升级的组合控件
    root.geometry('1408x792')
    root.title("字幕名字修改器")
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()

