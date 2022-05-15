import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog



win_list_dir = tk.Tk()
min_size_w = 300
min_size_h = 200
win_list_dir.geometry(f"{min_size_w}x{min_size_h}+156+50")
win_list_dir.title("Директории для поиска")
win_list_dir.grid_columnconfigure(0, weight=1)
win_list_dir.grid_rowconfigure(0, weight=1)

list_dir = tk.Listbox(win_list_dir, height=5)
list_dir.grid(column=0, row=0, sticky="nwes")
list_dir_scroll = ttk.Scrollbar(win_list_dir, orient=tk.VERTICAL, command=list_dir.yview)
list_dir_scroll.grid(column=1, row=0, sticky="ns")
list_dir['yscrollcommand'] = list_dir_scroll.set
list_dir_frame = ttk.Frame(win_list_dir)
list_dir_frame.grid(column=0, columnspan=2, row=1, sticky="we")
list_dir_frame.columnconfigure(0, weight=1)
list_dir_frame.columnconfigure(1, weight=1)
list_dir_frame.columnconfigure(2, weight=1)
btn_dir = tk.Button(list_dir_frame, text="Выбор")
btn_find = tk.Button(list_dir_frame, text="Поиск")
btn_list_can = tk.Button(list_dir_frame, text="Выход")
btn_dir.grid(column=0, row=0, sticky="we")
btn_find.grid(column=1, row=0, sticky="we")
btn_list_can.grid(column=2, row=0, sticky="we")


for i in range(1,101):
    list_dir.insert('end', 'Line %d of 100' % i)
list_dir.mainloop()



# dirname = filedialog.askdirectory(title="Выбрать директорию где искать файлы")
# print(dirname)






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


