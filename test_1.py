import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import pprint

def list_files_from_server():

    def select_dir():
        dirname = filedialog.askdirectory(parent=win_list_dir, title="Выбрать директорию где искать файлы", initialdir='Z:/Аудио')
        if dirname != "" and dirname not in list_dir_data_user.get():
            list_dir.insert('end', dirname)
            print(dirname)
        else:
            print("ничего не выбрано")

    def del_dir():
        if list_dir.curselection() != ():
            list_dir.delete(list_dir.curselection()[0])

    def search_return():
        win_list_dir.destroy()
        list_dir_data = []

    def btn_search_clc():
        aud_files = ['.wav', '.mp3', '.m4a', '.sfv', '.m4v', '.flac', '.wma', '.aiff', '.aif', '.aac', '.mp4','.ogg']
        nonlocal list_dir_data
        list_all_files = []
        if find_subdirs.get():
            pass
            # тут надо убрать подкаталоги, если они заданы при просмотре с поддирректориями и пересекаются
        for dir_for_search in list_dir_data_user.get():
            print(dir_for_search)



        # if find_subdirs.get():
        #     tmp = os.walk(list_dir_data_user.get()[list_dir.curselection()[0]])
        #     for el in tmp:
        #         tmp_path = os.path.normpath(el[0])
        #         tmp_path = os.path.normcase(tmp_path)
        #         for file in el[2]:
        #             tmp_file = file.lower()
        #             if tmp_file[tmp_file.rfind("."):] in aud_files:
        #                 list_all_files.append((tmp_path, tmp_file))
        #         # print(el)
        #         # print(os.path.normpath(el[0]))
        #
        #
        #     pprint.pprint(list_all_files)
        # else:
        #     tmp = os.listdir(list_dir_data_user.get()[list_dir.curselection()[0]])
        #
        #
        #     pprint.pprint(os.listdir(list_dir_data_user.get()[list_dir.curselection()[0]]))


    win_list_dir = tk.Tk()
    min_size_w = 300
    min_size_h = 200
    win_list_dir.geometry(f"{min_size_w}x{min_size_h}+156+50")
    win_list_dir.title("Директории для поиска")
    win_list_dir.grid_columnconfigure(0, weight=1)
    win_list_dir.grid_rowconfigure(0, weight=1)
    list_dir_data = []
    list_dir_data_user = tk.Variable(value=list_dir_data)
    list_dir = tk.Listbox(win_list_dir, height=5, listvariable=list_dir_data_user)
    list_dir.grid(column=0, row=0, sticky="nwes")
    list_dir_scroll = ttk.Scrollbar(win_list_dir, orient=tk.VERTICAL, command=list_dir.yview)
    list_dir_scroll.grid(column=1, row=0, sticky="ns")
    list_dir['yscrollcommand'] = list_dir_scroll.set
    list_dir_scroll_hor = tk.Scrollbar(win_list_dir, orient=tk.HORIZONTAL, command=list_dir.xview)
    list_dir_scroll_hor.grid(column=0, row=1, columnspan=2, sticky="we")
    list_dir['xscrollcommand'] = list_dir_scroll_hor.set
    list_dir_frame = ttk.Frame(win_list_dir)
    list_dir_frame.grid(column=0, columnspan=2, row=2, sticky="we")
    for i in range(4):
        list_dir_frame.columnconfigure(i, weight=1)
    # list_dir_frame.rowconfigure(0)
    find_subdirs = tk.BooleanVar(value=True)
    chk_btn_subdir = tk.Checkbutton(list_dir_frame, text="Искать в поддиреекториях", variable=find_subdirs)
    chk_btn_subdir.grid(column=0, row=0, columnspan=4, sticky="we" )
    btn_dir = tk.Button(list_dir_frame, text="Добавить", command=select_dir)
    btn_dir_del = tk.Button(list_dir_frame, text="Удалить", command=del_dir)
    btn_find = tk.Button(list_dir_frame, text="Поиск", command=btn_search_clc)
    btn_list_can = tk.Button(list_dir_frame, text="Выход", command=search_return)
    btn_dir.grid(column=0, row=1, sticky="we")
    btn_dir_del.grid(column=1, row=1, sticky="we")
    btn_find.grid(column=2, row=1, sticky="we")
    btn_list_can.grid(column=3, row=1, sticky="we")

    list_dir.mainloop()

    print(list_dir_data_user.get())
    print(find_subdirs.get())

    return


    # dirname = filedialog.askdirectory(title="Выбрать директорию где искать файлы")
    # print(dirname)

if __name__ == '__main__':
    list_files_from_server()



    #
    # class FoundAllFiles():
    #     f_loc = r'C:\Users\micrab\AppData\Local\Temp\gen_py'
    #     all_dir = os.listdir(f_loc)
    #     if len(all_dir) != 0:
    #         for f in all_dir:
    #             if os.path.isfile(f_loc + chr(92) + f):
    #                 os.remove(f_loc + chr(92) + f)
    #             else:
    #                 rmtree(f_loc + chr(92) + f)


