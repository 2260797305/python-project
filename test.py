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
        self.cur_format = ""
        self.last_dir = None
        self.filter_entry_list = []

        # Radiobutton, subtitle type
        lable1 = Label(master, text='字幕封装类型：  ')
        lable1.place(x=10, y=10)

        self.subttitle_type = IntVar(value=-1)
        # self.subttitle_type.set(-1)

        self.no_sub = Radiobutton(master, text='无字幕', fg='blue', variable=self.subttitle_type, value=NO_SUB, command=self.sub_select)
        self.no_sub.place(x=120, y=10)

        self.inline_sub = Radiobutton(master, text='内嵌', fg='blue', variable=self.subttitle_type, value=INLINE_SUB, command=self.sub_select)
        self.inline_sub.place(x=200, y=10)

        self.inside_sub = Radiobutton(master, text='内封', fg='blue', variable=self.subttitle_type, value=INSIDE_SUB, command=self.sub_select)
        self.inside_sub.place(x=280, y=10)

        self.outside_sub = Radiobutton(master, text='外挂', fg='blue', variable=self.subttitle_type, value=OUTSIDE_SUB, command=self.sub_select)
        self.outside_sub.place(x=360, y=10)

        # Radiobutton, subtitle type
        lable_ro = Label(master, text='分辨率：')
        lable_ro.place(x=460, y=10)

        self.rotion_type = StringVar()
        self.ro_720 = Radiobutton(master, text='720P', fg='blue', variable=self.rotion_type, value="[720P]", command=self.sub_select)
        self.ro_720.place(x=520, y=10)

        self.ro_1080 = Radiobutton(master, text='1080P', fg='blue', variable=self.rotion_type, value="[1080P]", command=self.sub_select)
        self.ro_1080.place(x=600, y=10)

        self.ro_xx = Radiobutton(master, text='unknown', fg='blue', variable=self.rotion_type, value="unknown", command=self.sub_select)
        self.ro_xx.place(x=680, y=10)

        # sCheckbutton, subtitle species
        lable2 = Label(master, text='字幕语言：  ')
        lable2.place(x=10, y=45)

        self.subtitle_species_CH = StringVar()
        self.subtitle_species_CH.set("")

        self.box_ch = Checkbutton(master, text='中文', variable=self.subtitle_species_CH, onvalue='Ch', offvalue="", command=self.sub_select)
        self.box_ch.place(x=120, y=45)

        self.subtitle_species_JP = StringVar()
        self.subtitle_species_JP.set("")
        self.box_jp = Checkbutton(master, text='日语', variable=self.subtitle_species_JP, onvalue='Jp', offvalue="", command=self.sub_select)
        self.box_jp.place(x=200, y=45)

        self.subtitle_split = IntVar()
        self.box_split = Checkbutton(master, text='字幕分离', variable=self.subtitle_split, onvalue=1, offvalue=0, command=self.sub_select)
        self.box_split.place(x=280, y=45)

        # dir input
        lable3 = Label(master, text='解析目录：  ')
        lable3.place(x=10, y=80)

        self.dir_line = Entry(master, textvariable=self.dir, width=60)
        self.dir_line.place(x=120, y=80)
        self.dir_line.bind('<Return>', self.dir_input)

        self.open_button = Button(master, text="open", command=self.open_file, width=11)
        self.open_button.place(x=560, y=76)

        self.rename_folder_button = Button(master, text="文件夹重命名", command=self.rename_folder, width=11)
        self.rename_folder_button.place(x=560, y=144)

        # folder name
        lable4 = Label(master, text='文件夹名称：  ')
        lable4.place(x=10, y=115)

        self.folder_name_line = Entry(master, textvariable=self.folder_name, width=60)
        self.folder_name_line.place(x=120, y=115)
        self.folder_name_line.bind('<Return>', self.name_change)
        self.folder_name_line.bind('<FocusOut>', self.name_change)

        # dir output
        lable5 = Label(master, text='输出目录：  ')
        lable5.place(x=10, y=150)

        self.out_dir_line = Entry(master, textvariable=self.out_dir, width=60, state="readonly")
        self.out_dir_line.place(x=120, y=150)

        # old filter
        lable6 = Label(master, text='原名字：  ')
        lable6.place(x=10, y=220)

        lable6_1 = Label(master, text='固定开始字符')
        lable6_1.place(x=120, y=195)
        self.old_start = Entry(master, width=30)
        self.old_start.place(x=120, y=220)
        self.filter_entry_list.append(self.old_start)

        lable6_2 = Label(master, text='变量')
        lable6_2.place(x=360, y=195)

        self.old_var = Entry(master, width=10)
        self.old_var.place(x=360, y=220)
        self.old_var.bind('<Key>', self.filter_change)

        lable6_3 = Label(master, text='固定后置字符')
        lable6_3.place(x=460, y=195)
        self.old_var_end = Entry(master, width=30)
        self.old_var_end.place(x=460, y=220)
        self.filter_entry_list.append(self.old_var_end)

        lable6_4 = Label(master, text='变化字符')
        lable6_4.place(x=700, y=195)
        self.old_flexible_end = Entry(master, width=30)
        self.old_flexible_end.place(x=700, y=220)

        lable6_5 = Label(master, text='固定结束字符')
        lable6_5.place(x=930, y=195)
        self.old_end = Entry(master, width=30)
        self.old_end.place(x=930, y=220)
        self.filter_entry_list.append(self.old_end)

        lable6_6 = Label(master, text='↓↓↓↓↓')
        lable6_6.place(x=550, y=260)

        # new filter
        lable7 = Label(master, text='新名字：  ')
        lable7.place(x=10, y=320)

        lable7_1 = Label(master, text='固定开始字符')
        lable7_1.place(x=120, y=295)
        self.new_start = Entry(master, width=30)
        self.new_start.place(x=120, y=320)
        self.filter_entry_list.append(self.new_start)

        lable7_2 = Label(master, text='变量')
        lable7_2.place(x=360, y=295)

        self.new_var = Entry(master, width=10)
        self.new_var.place(x=360, y=320)
        self.new_var.bind('<Key>', self.filter_change)

        lable7_3 = Label(master, text='固定后置字符')
        lable7_3.place(x=460, y=295)
        self.new_var_end = Entry(master, width=30)
        self.new_var_end.place(x=460, y=320)
        self.new_var_end.bind('<Return>', self.filter_change)
        # self.new_var_end.bind('<Control - V>', self.filter_change)
        # self.new_var_end.bind('<Control - X>', self.filter_change)

        lable7_4 = Label(master, text='变化字符')
        lable7_4.place(x=700, y=295)
        self.new_flexible_end = Entry(master, width=30)
        self.new_flexible_end.place(x=700, y=320)
        self.filter_entry_list.append(self.new_flexible_end)

        lable7_5 = Label(master, text='固定结束字符')
        lable7_5.place(x=931, y=295)
        self.new_end = Entry(master, width=30)
        self.new_end.place(x=931, y=320)
        self.filter_entry_list.append(self.new_end)

        for entry in self.filter_entry_list:
            entry.bind('<Return>', self.filter_change)
            entry.bind('<FocusOut>', self.filter_change)
            # entry.bind('<Control - V>', self.filter_change)
            # entry.bind('<Control - X>', self.filter_change)

        lable9 = Label(master, text='选中文件名：  ')
        lable9.place(x=10, y=360)
        self.file_full_name = Entry(master, width=146, textvariable=self.select_full_name, state="readonly")
        self.file_full_name.place(x=120, y=360)

        lable8 = Label(master, text='格式过滤：  ')
        lable8.place(x=10, y=395)
        self.fmt_list_box = Listbox(master, width=12, height=1)
        self.fmt_list_box.place(x=10, y=430)
        self.fmt_list_box.bind('<Double-Button-1>', self.format_list_select)

        self.sbx = Scrollbar(root, orient=HORIZONTAL)
        # sbx.pack(side=BOTTOM, fill=X)
        self.sby = Scrollbar(root, orient=VERTICAL)
        #sby.pack(side=RIGHT, fill=Y)
        self.sby.place(x=1230, y=395, width=16, height=300)
        self.sbx.place(x=120, y=690, width=1120, height=16)

        self.cur_show_list_box = Listbox(master, xscrollcommand=self.xxx_scroll, yscrollcommand=self.yyy_scroll, width=75, height=16)
        self.cur_show_list_box.place(x=120, y=395)
        self.cur_show_list_box.bind('<Double-Button-1>', self.file_select)
        self.sbx.config(command=self.xxx_set_view)
        self.sby.config(command=self.yyy_set_view)

        self.covert_button = Button(master, text=">>>", command=self.rename_file)
        self.covert_button.place(x=656, y=515)
        
        self.file_modify_name = Listbox(master, xscrollcommand=self.xxx_scroll, yscrollcommand=self.yyy_scroll, width=75, height=16)
        # self.file_modify_name.grid(row=13, column=4)
        self.file_modify_name.place(x=700, y=395)
        self.disable_all()

    def xxx_set_view(self, *args):
        self.cur_show_list_box.xview(*args)
        self.file_modify_name.xview(*args)

    def yyy_set_view(self, *args):
        print(*args)
        self.cur_show_list_box.yview(*args)
        self.file_modify_name.yview(*args)

    def xxx_scroll(self, a, b):
        self.sbx.set(a, b)
        self.cur_show_list_box.xview_moveto(a)
        self.file_modify_name.xview_moveto(a)

    def yyy_scroll(self, a, b):
        self.sby.set(a, b)
        self.cur_show_list_box.yview_moveto(a)
        self.file_modify_name.yview_moveto(a)

    def name_change(self, evt):
        self.sub_select()

    def dir_input(self, evt):
        print(self.dir.get())
        if not os.path.isdir(self.dir.get()):
            print("no such dir")
            tkinter.messagebox.showerror(title='Error', message='无效的路径')
            self.disable_all()
            return
        else:
            self.prser_dir()

    def filter_change(self, evt):
        if len(self.fmt_file_list) == 0:
            return
        print(evt)
        print(self.old_start.get())
        self.parser_file_list()

    def format_list_select(self, evt):
        tu = self.fmt_list_box.curselection()
        if tu.__len__() > 0:
            idx = self.fmt_list_box.curselection()[0]
            if self.cur_format == self.fmt_list_box.get(idx):
                return

            self.cur_format = self.fmt_list_box.get(idx)
            self.fmt_file_list.clear()
            self.cur_show_list_box.delete(0, END)
            self.file_modify_name.delete(0, END)
            self.select_full_name.set("")
            print(self.cur_format)
            for i in self.file_list:
                if os.path.splitext(i)[1] == self.cur_format:
                    self.fmt_file_list.append(i)
                    self.cur_show_list_box.insert(END, i)
            self.parser_file_list()

    def file_select(self, evt):
        tu = self.cur_show_list_box.curselection()
        if tu.__len__() > 0:
            self.file_full_name.delete(0, END)
            idx = self.cur_show_list_box.curselection()[0]
            full_name = self.cur_show_list_box.get(idx)
            self.select_full_name.set(os.path.splitext(full_name)[0])
            print(full_name)
            self.parser_file_list()

    def sub_select(self):
        print(self.rotion_type.get())
        if self.rotion_type.get() == "unknown":
            self.fold_name_prefix = ""
        else:
            self.fold_name_prefix = self.rotion_type.get()

        if self.subttitle_type.get() == NO_SUB:
            self.fold_name_prefix += "[无字幕]"
            self.box_ch['state'] = DISABLED
            self.box_ch.deselect()
            self.box_jp['state'] = DISABLED
            self.box_jp.deselect()
            self.box_split['state'] = DISABLED
            self.box_split.deselect()
        else:
            self.box_ch['state'] = ACTIVE
            self.box_jp['state'] = ACTIVE

            if self.subttitle_type.get() == INLINE_SUB:
                self.fold_name_prefix += "[内嵌]"
            elif self.subttitle_type.get() == INSIDE_SUB:
                self.fold_name_prefix += "[内封]"
            elif self.subttitle_type.get() == OUTSIDE_SUB:
                self.fold_name_prefix += "[外挂]"
            else:
                return

        if self.subtitle_species_CH.get() != "" and self.subtitle_species_JP.get() != "" and self.subttitle_type.get() != INLINE_SUB:
            self.box_split['state'] = ACTIVE
        else:
            self.box_split['state'] = DISABLED
            self.box_split.deselect()

        if self.subtitle_split.get() == 1:
            if self.subtitle_species_CH.get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.subtitle_species_CH.get() + "]"
            if self.subtitle_species_JP.get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.subtitle_species_JP.get() + "]"
        else:
            if self.subtitle_species_CH.get() != "":
                self.fold_name_prefix = self.fold_name_prefix + "[" + self.subtitle_species_CH.get()
                if self.subtitle_species_JP.get() != "":
                    self.fold_name_prefix = self.fold_name_prefix + "&&" + self.subtitle_species_JP.get()

                self.fold_name_prefix = self.fold_name_prefix + "]"
            else:
                if self.subtitle_species_JP.get() != "":
                    self.fold_name_prefix = self.fold_name_prefix + "[" + self.subtitle_species_JP.get() + "]"

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
        self.no_sub['state'] = ACTIVE
        self.inline_sub['state'] = ACTIVE
        self.inside_sub['state'] = ACTIVE
        self.outside_sub['state'] = ACTIVE
        self.ro_1080['state'] = ACTIVE
        self.ro_720['state'] = ACTIVE
        self.ro_xx['state'] = ACTIVE

        self.rename_folder_button['state'] = ACTIVE

        self.fmt_list_box.delete(0, END)
        self.cur_show_list_box.delete(0, END)
        self.file_modify_name.delete(0, END)
        self.file_list.clear()

        self.folder_name.set(os.path.basename(self.dir.get()))
        self.out_dir.set(os.path.dirname(self.dir.get()) + "/" + self.folder_name.get() + self.fold_name_prefix)
        dir_path = self.dir.get()

        print("list the file")
        print(dir_path)
        file_list = os.listdir(dir_path)
        file_format = []
        print(file_list)
        for i in file_list:
            t = self.dir.get() + "/" + i
            if os.path.isfile(t):
                #print(i)
                self.file_list.append(i)
                format = os.path.splitext(i)[1]
                if format not in file_format:
                    file_format.append(format)
                    self.fmt_list_box.insert(END, format)

        self.rename_folder_button['state'] = ACTIVE
        if len(file_format) < 10:
            self.fmt_list_box['height'] = len(file_format)
        else:
            self.fmt_list_box['height'] = 10
        self.last_dir = dir_path
        # print(self.file_list)

    def disable_all(self):
        self.subttitle_type.set(-1)
        self.no_sub['state'] = DISABLED
        self.no_sub.deselect()

        self.inline_sub['state'] = DISABLED
        self.inline_sub.deselect()

        self.inside_sub['state'] = DISABLED
        self.inside_sub.deselect()

        self.outside_sub['state'] = DISABLED
        self.outside_sub.deselect()

        self.rotion_type.set("unknown")

        self.ro_720['state'] = DISABLED
        # self.ro_720.deselect()
        #
        self.ro_1080['state'] = DISABLED
        # self.ro_1080.deselect()
        #
        self.ro_xx['state'] = DISABLED
        # self.ro_xx.deselect()



        self.box_ch['state'] = DISABLED
        self.box_ch.deselect()
        self.box_jp['state'] = DISABLED
        self.box_jp.deselect()
        self.box_split['state'] = DISABLED
        self.box_split.deselect()
        self.rename_folder_button['state'] = DISABLED
        self.covert_button['state'] = DISABLED

        self.out_dir_line.delete(0, END)
        self.folder_name_line.delete(0, END)
        self.fmt_list_box.delete(0, END)
        self.cur_show_list_box.delete(0, END)
        self.file_modify_name.delete(0, END)
        self.file_list.clear()
        self.select_full_name.set("")
        self.cur_format = ""
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

    def rename_file(self):
        t = tkinter.messagebox.askokcancel('文件重命名', "是否确定重命名列表中的文件??")  # 确定/取消，返回值true/false
        if not t:
            return
        file_1 = self.cur_show_list_box.get(0, END)
        file_2 = self.file_modify_name.get(0, END)
        if len(file_1) != len(file_2):
            print("error file")
            return
        id = 0
        while id < len(file_1):
            old = self.dir.get() + "/" + file_1[id]
            new = self.dir.get() + "/" + file_2[id]
            if old != new:
                if os.path.isfile(old) and (not os.path.isfile(new)):
                    print(old)
                    print(new)
                    os.rename(old, new)
                else:
                    t = tkinter.messagebox.askokcancel('文件重命名', "有已经存在的文件名 %s\n是否覆盖?" % new)  # 确定/取消，返回值true/false
            id += 1
        self.prser_dir()

    def find_eigenvalues(self, file_name, file_list):
        start_value_list = []
        var_value_list = []
        var_end_list = []
        flex_value_list = []
        end_value_list = []
        len_name = len(file_name)

        for i in file_list:
            jujde_name = os.path.splitext(i)[0]
            if file_name == jujde_name:
                continue

            # find start value
            cnt = 0
            while cnt < len_name:
                t_str = file_name[0:cnt]
                if jujde_name.startswith(t_str):
                    find = 0
                    for v in start_value_list:
                        if t_str == v[0]:
                            v[1] += 1
                            find = 1
                            break
                    if find == 0:
                        start_value_list.append([t_str, 1])
                    print(file_name + " vs " + jujde_name + " = " + t_str)
                    cnt += 1
                else:
                    break
                    
        print(start_value_list)
        self.old_start.insert(END, "aaa")

    def parser_file_list(self):
        self.file_modify_name.delete(0, END)
        self.cur_show_list_box.delete(0, END)

        old_start = self.old_start.get()
        old_var = self.old_var.get()
        old_var_end = self.old_var_end.get()
        old_flexible_end = self.old_flexible_end.get()
        old_end = self.old_end.get()

        new_star = self.new_start.get()
        new_var = self.new_var.get()
        new_var_end = self.new_var_end.get()
        new_flexible_end = self.new_flexible_end.get()
        new_end = self.new_end.get()

        select_cnt = 0

        for i in self.fmt_file_list:
            name = os.path.splitext(i)[0]
            s = 0
            e = len(name)
            var = new_star
            while 1:
                if old_start != "":
                    if name.startswith(old_start):
                        s += len(old_start)
                    else:
                        break
                if old_end != "":
                    if name.endswith(old_end):
                        e -= len(old_end)
                    else:
                        break
                if old_var_end != "":
                    t = name[s:e].find(old_var_end)
                    if t != -1:
                        var += name[s:s+t] + new_var_end
                        s += t
                    else:
                        break
                var += name[s:e]
                new_name = var + new_end + os.path.splitext(i)[1]
                self.cur_show_list_box.insert(END, i)
                self.file_modify_name.insert(END, new_name)
                select_cnt += 1
                break
        if select_cnt == 0:
            self.covert_button['state'] = DISABLED
        else:
            self.covert_button['state'] = ACTIVE

if __name__ == '__main__':
    root = Tk()
    root.tk.eval('package require Tix')  # 引入升级包，这样才能使用升级的组合控件
    root.geometry('1280x720')
    root.title("文件批量重命名")
    root.resizable(width=False, height=False)
    app = App(root)
    root.mainloop()

