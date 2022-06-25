import tkinter as tk
from tkinter import messagebox
from devicedata import full_program_list, full_decoder_list
from tkinter import ttk
import requests
import datetime
from io import BytesIO
from PIL import Image, ImageTk
import os
from random import choice

# эти три строки позволяют показывать свою иконку при запуске программы
# когда запускается приложение, Windows смотрит на исполняемый файл и пытается угадать, к какой application group оно принадлежит.
# По умолчанию все скрипты Python сгруппированы в одну и ту же группу "Python" , поэтому будет отображаться значок Python.
# # Чтобы это не происходило, нам нужно предоставить Windows другой идентификатор приложения.
import ctypes
myappid = 'micrab.remote.yamacha.version01'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# import json
# import pprint

cod_error = "error"
volume_max = 0
volume_min = -80.5
volume_step = 0.5
volume_calc = 0
scale_use = True  # установка шкалы
net_usb_list = ['airplay', 'mc_link', 'server', 'net_radio', 'bluetooth', 'usb'] # что доступно из входов для выбора ресурсов
chk_file = False # для записи пометки в файле истории проигрывания по кнопке чек
aud_files = ['.wav', '.mp3', '.m4a', '.sfv', '.m4v', '.flac', '.wma', '.aiff', '.aif', '.aac', '.mp4', '.ogg']
dirs_w_audio = ('Z:/Аудио/Музыка', 'Z:/Аудио/Музыка 2')
last_play_pic = ""

try:
    with open("play_history.txt") as his_file:
        for line in his_file:
            pass
        last_play = line
        last_play = last_play[20:last_play.rfind("\t")]
except FileNotFoundError:
    last_play = ""

try:
    with open("play_history_dir.txt") as his_file:
        for line in his_file:
            pass
        last_path = line
        last_path = last_path[20:-1]
except FileNotFoundError:
    last_path = ""

dev_url = "http://192.168.50.156"

def device_connect(add_link):
    """Связь с устройством, на входе часть адреса на выходе ошибка или ответ устройства"""
    global cod_error
    link = f"{dev_url}/YamahaExtendedControl"
    link = link + add_link
    try:
        responce = requests.get(link, timeout=10)
        if responce.status_code == 200:
            if responce.json()["response_code"] != 0:
                messagebox.showinfo(message=f"Ошибка команды, ответ: {responce.json()['response_code']}")
                return cod_error
            else:
                return responce
        else:
            messagebox.showinfo(message=f"Ошибка в ответе на {add_link} от устройства, ответ: {responce}")
            return cod_error
    except requests.exceptions.ConnectTimeout:
        messagebox.showinfo(message='Не могу найти устройство по указанному адресу')
        exit("Неверный адрес устройства")


def show_time(sec):
    """вывод времени на входе целое число в секундах на выходе строка вида чч:мм:сс"""
    s = sec % 60
    sec -= s
    m = sec // 60 % 60
    h = sec // 60 - m
    h = h // 60
    return f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"


def dec_in_doble(n):
    """перевод десятичного (на входе) в двоичное (на выходе словари по битам) """
    attr_in_double_sys = []
    while n > 0:
        attr_in_double_sys.append(n % 2)
        n = n // 2
    return attr_in_double_sys


wind = tk.Tk()
wind.title("Yamaha RX-V485")
wind_photo = tk.PhotoImage(file = "device.png")
wind.iconphoto(False, wind_photo)
min_size_w = 300
min_size_h = 750
wind.geometry(f"{min_size_w}x{min_size_h}+156+50")
wind.minsize(min_size_w, min_size_h)
wind.columnconfigure(0, minsize = min_size_w-4, weight=0)
wind.resizable(False, True)

level_row = 0

def btn_power_clc():
    chk_window()
    match power:
        case "on":
            device_connect("/v2/main/setPower?power=standby")
        case "standby":
            device_connect("/v2/main/setPower?power=on")
        case "toggle":
            while power == "toggle":
                chk_window()
    chk_window()


loc_frame_row = 1
frame_power = ttk.Labelframe(wind, text='Вкл/выкл', width=min_size_w-10)
frame_power.grid(column=0, row=level_row, sticky="nesw", padx = 3)
btn_power = tk.Button(frame_power, command=btn_power_clc)
btn_power_photo_on = tk.PhotoImage(file = "power_on_red.png")
btn_power_photo_off = tk.PhotoImage(file = "power_on.png")
btn_power.grid(column=0, padx = 3)
level_row += loc_frame_row


def scale_vollume_clc(vol):
    global scale_use
    scale_use = False
    volume_calc_set = int((float(vol)-volume_min) / volume_step)
    device_connect(f"/v2/main/setVolume?volume={volume_calc_set}")

def btn_volume_down_clc():
    chk_window()
    if actual_volume["value"] > volume_min:
        device_connect("/v2/main/setVolume?volume=down")
        chk_window()

def btn_volume_up_clc():
    chk_window()
    if actual_volume["value"] < volume_max:
        device_connect("/v2/main/setVolume?volume=up")
        chk_window()

def btn_volume_mute_clc():
    chk_window()
    if mute:
        device_connect("/v2/main/setMute?enable=false")
    else:
        device_connect("/v2/main/setMute?enable=true")
    chk_window()


loc_frame_row = 2
loc_frame_col = 6
frame_volume = ttk.Labelframe(wind, text='Громкость', width=min_size_w-10)
frame_volume.grid(column=0, row=level_row, rowspan=loc_frame_row, sticky="nesw", padx=3)
for i in range (loc_frame_col-1):
    frame_volume.columnconfigure(i, minsize=(min_size_w-10)//loc_frame_col, weight=1)
scale_var = tk.DoubleVar()
scale_volume = tk.Scale(frame_volume, orient="horizontal", resolution= volume_step, from_= volume_min,
                        to=volume_max, command=scale_vollume_clc, variable=scale_var)
scale_volume.grid(row=0, column= 0, columnspan=loc_frame_col, sticky="nesw")

btn_volume_photo_up = tk.PhotoImage(file="sound_up.png")
btn_volume_photo_down = tk.PhotoImage(file="sound_down.png")
btn_volume_photo_mute_off = tk.PhotoImage(file="mute.png")
btn_volume_photo_mute_on = tk.PhotoImage(file="mute_on.png")
btn_volume_down = tk.Button(frame_volume, image=btn_volume_photo_down, command=btn_volume_down_clc)
btn_volume_down.grid(row = 1, column = 0, sticky="nesw",padx = 3)
btn_volume_up = tk.Button(frame_volume, image=btn_volume_photo_up, command=btn_volume_up_clc)
btn_volume_up.grid(row = 1, column = 4, sticky="nesw", padx = 3)
btn_volume_mute = tk.Button(frame_volume, command=btn_volume_mute_clc)
btn_volume_mute.grid(row = 1, column = 2, sticky="nesw", padx = 3)
level_row += loc_frame_row


def scale_image(picture_in, width=200, height=200):
    w, h = picture_in.size
    if w > width or h > height:
        max_size = (width, height)
        picture_in.thumbnail(max_size) #, Image.ANTIALIAS)
    return picture_in

def btn_input_list_clc():
    """ подпрограмма для создания и работы с окном выбора элементов из источника проигрывания"""

    max_line = 0  # для определения кол-ва элементов

    def wind_dismiss():
        """ перехват события нажатия на крестик и закрытие окна со снятием модальности"""
        wind_list.grab_release()
        wind_list.destroy()

    def wind_list_get_spisok():
        """ запрос к устройству и создание списка всех элементов в выбранном каталоге"""
        nonlocal max_line
        index_Start_in_list = 0
        max_line = 8
        last_max_line = 0
        list_info = []
        responce = cod_error
        btn_sel.config(state=tk.DISABLED)
        btn_can.configure(state=tk.DISABLED)
        while (max_line - index_Start_in_list) >= 0:
            responce = device_connect(f"/v2/netusb/getListInfo?input={dev_input_now.get()}&index={index_Start_in_list}&size=8&lang=ru")
            if responce != cod_error:
                index_Start_in_list += 8
                max_line = responce.json()["max_line"]
                if max_line != last_max_line:
                    last_max_line = max_line
                    process_bar.configure(maximum=max_line)
                tmp_index = index_Start_in_list if (index_Start_in_list+8 <= max_line) else max_line
                process_bar.configure(value=tmp_index)
                process_bar.update()
                for i in range(len(responce.json()["list_info"])):
                    list_info_tmp = responce.json()["list_info"][i]
                    list_info_tmp["attribute"] = dec_in_doble(list_info_tmp["attribute"])
                    list_info.append(list_info_tmp)
            else:
                break
        if responce != cod_error:
            menu_name = responce.json()["menu_name"]
            menu_layer = responce.json()["menu_layer"]
            max_line = responce.json()["max_line"]
        else:
            menu_name = ""
            menu_layer = 0
            max_line = 0

        # for el in list_info:
        #     print(el)

        btn_sel.config(state=tk.NORMAL)
        btn_can.configure(state=tk.NORMAL)

        return (menu_name, list_info, menu_layer)


    def show_picture(event):
        """ показ картинки каталога в окне для выбираемой позиции"""
        # nonlocal spisok_picture, frame_spisok
        if spisok.curselection() != ():
            frame_picture.configure(text=choices[spisok.curselection()[0]])
            if full_list[spisok.curselection()[0]]['attribute'][1] == 1:
                btn_sel.configure(text="Открыть")
            elif full_list[spisok.curselection()[0]]['attribute'][2] == 1:
                btn_sel.configure(text="Играть")
            else:
                btn_sel.configure(text="Выбрать")
            if full_list[spisok.curselection()[0]]['thumbnail'] != "" and full_list[spisok.curselection()[0]]['attribute'][1] == 1:
                image_bite = requests.get(full_list[spisok.curselection()[0]]['thumbnail'], timeout=10)
                # print(f"запрос {image_bite.url} ответ: {image_bite.status_code}")
                if image_bite.status_code == 200:
                    pil_image = Image.open(BytesIO(image_bite.content))
                    image = ImageTk.PhotoImage(scale_image(pil_image))
                    # label.config(image=image, text='')
                    # spisok_image.configure(data=image_bite.content)
                    spisok_picture.configure(image=image, text="")
                    spisok_picture.image = image # строка чтобы картинка не улетала в мусор после завершения подпрограммы
            else:
                spisok_picture.configure(image="")
        else:
            frame_picture.configure(text=wind_name)
            spisok_picture.configure(image="")

    def wind_list_update(wind_name, full_list, menu_level):
        """обновление списка в виджете и вывод его на экран"""
        nonlocal choices, max_line
        wind_name = wind_name + " - элементов: " + str(max_line)
        frame_spisok.configure(text=wind_name)
        choices = [el['text'] for el in full_list]
        choicesvar.set(choices)
        for i in range(len(choices)):
            if full_list[i]['attribute'][1] == 1:
                spisok.itemconfigure(i, background='#f0f0ff')
            else:
                spisok.itemconfigure(i, background="white")
        responce = device_connect("/v2/netusb/getRecentInfo").json()
        last_song = 0
        if responce != cod_error:
            try:
                last_song = choices.index(responce['recent_info'][0]['text'])
            except ValueError:
                last_song = 0
        spisok.selection_clear(0, len(choices))
        spisok.select_set(last_song)
        spisok.see(last_song)
        spisok.index(last_song)
        spisok.activate(last_song)
        if menu_level == 0:
            btn_can.configure(text="Закрыть")
        else:
            btn_can.configure(text="Назад")
        show_picture("")

    def btn_can_clc():
        nonlocal full_list, wind_name, menu_level
        if menu_level == 0:
            wind_dismiss()
        else:
            responce = device_connect("/v2/netusb/setListControl?list_id=main&type=return")
            if responce != cod_error:
                wind_name, full_list, menu_level = wind_list_get_spisok()
                wind_list_update(wind_name, full_list, menu_level)

    def btn_sel_clc_dub(event):
        btn_sel_clc()


    def btn_sel_clc():
        nonlocal full_list, wind_name, menu_level
        if spisok.curselection() == ():
            messagebox.showinfo(title="Ничего не выбрано!", message="Сначала выберите строчку, а потом нажимайте кнопку Открыть/Играть или нажмите кнопку Назад/Закрыть")
            return
        if full_list[spisok.curselection()[0]]['attribute'][1] == 1:
            responce = device_connect(f"/v2/netusb/setListControl?list_id=main&type=select&index={spisok.curselection()[0]}")
            if responce != cod_error:
                wind_name, full_list, menu_level = wind_list_get_spisok()
                wind_list_update(wind_name, full_list, menu_level)
        elif full_list[spisok.curselection()[0]]['attribute'][2] == 1:
            # играть композицию
            device_connect(f"/v2/netusb/setListControl?list_id=main&type=play&index={spisok.curselection()[0]}")
            # print("выбрана композиция")
        else:
            messagebox.showinfo(title="Ошибка!",
                                message="Позиция не открывается и не играет, надо выбрать другую")
            # print("не открывается и не играет")
            # btn_sel.configure(text="Выбрать")
        # print(menu_level)
        if menu_level == 0:
            btn_can.configure(text="Закрыть")
        else:
            btn_can.configure(text="Назад")


    # "http://{host}/YamahaExtendedControl/v1/netusb/setListControl?list_id=main&type=select&index=1"


    wind_list = tk.Toplevel(wind)
    wind_list.title("Выбор ресурса для проигрывания")
    wind_list.geometry(f'{min_size_w+50}x{min_size_h-20}+{wind.winfo_x() + 10}+{wind.winfo_y() + 10}')  # положение окна на 10 точек смещения от основного окна
    wind_list.minsize(min_size_w+50, min_size_h-20)
    wind_list_photo = tk.PhotoImage(file="server.png")
    wind_list.iconphoto(False, wind_list_photo)
    wind_name = ""
    full_list = []
    menu_level = 0
    wind_list.columnconfigure(0, weight=1)
    wind_list.rowconfigure(0, weight=0)
    wind_list.rowconfigure(1, weight=0)
    wind_list.rowconfigure(2, weight=0)
    wind_list.rowconfigure(3, weight=0)
    frame_spisok = ttk.Labelframe(wind_list, text=wind_name)
    frame_spisok.grid(column=0, row=0, sticky="nesw", padx=3)
    frame_spisok.columnconfigure(0, weight=1)
    # frame_spisok.rowconfigure(0, weight=1)
    choices = [] # [el['text'] for el in full_list]
    choicesvar = tk.Variable(value=choices)
    spisok = tk.Listbox(frame_spisok, height=20 , listvariable=choicesvar)
    spisok.grid(column=0, row=0, sticky="nesw")
    vert_scroll = tk.Scrollbar(frame_spisok, orient=tk.VERTICAL, command=spisok.yview)
    vert_scroll.grid(column=1, row=0, sticky="ns")
    spisok['yscrollcommand'] = vert_scroll.set
    hor_scroll = tk.Scrollbar(frame_spisok, orient=tk.HORIZONTAL, command=spisok.xview)
    hor_scroll.grid(column=0, row=1, sticky="we")
    spisok['xscrollcommand'] = hor_scroll.set
    frame_progress = ttk.Labelframe(wind_list, text="загрузка")
    frame_progress.grid(column=0, row=1, sticky="ew", padx=3)
    frame_progress.columnconfigure(0, weight=1)
    # frame_progress.rowconfigure(0, weight=0)
    process_bar = ttk.Progressbar(frame_progress, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=100, value=0)
    process_bar.grid(column=0, row=0, sticky="nesw")

    frame_picture = ttk.Labelframe(wind_list, text=wind_name, width=200, height=200)
    frame_picture.grid(column=0, row=2, sticky="nswe", padx=3)
    frame_picture.columnconfigure(0, weight=1)
    frame_picture.rowconfigure(0, weight=1)
    # spisok_image = tk.PhotoImage()
    # spisok_picture_info = tk.StringVar()
    spisok_picture = tk.Label(frame_picture)
    spisok_picture.grid(row=0, column=0, sticky="nswe", padx=3)
    spisok.bind('<<ListboxSelect>>', show_picture)
    spisok.bind('<Double-1>', btn_sel_clc_dub)
    frame_buttons = ttk.Labelframe(wind_list, text='Функции:')
    frame_buttons.columnconfigure(0, weight=1)
    frame_buttons.columnconfigure(1, weight=1)
    frame_buttons.grid(column=0, row=3, sticky="nesw", padx=3)
    btn_sel = tk.Button(frame_buttons, text="Выбрать", command=btn_sel_clc)
    btn_sel.grid(row=0, column=0, sticky="nswe", padx=3)
    btn_can = tk.Button(frame_buttons, text="Закрыть", command=btn_can_clc)
    # if menu_level == 0:
    #     btn_can.configure(text="Закрыть")
    # else:
    #     btn_can.configure(text="Назад")
    btn_can.grid(row=0, column=1, sticky="nswe", padx=3)

    wind_name, full_list, menu_level = wind_list_get_spisok()
    wind_list_update(wind_name, full_list, menu_level)

    # frame_spisok.configure(text="test")


    # эти пять строчек делают окно модальным, их надо поместить вниз(в конце) команд
    wind_list.protocol("WM_DELETE_WINDOW", wind_dismiss)  # intercept close button
    wind_list.transient(wind)  # dialog window is related to main
    wind_list.wait_visibility() # can't grab until window appears, so we wait
    wind_list.grab_set() # ensure all input goes to our window
    wind_list.focus_set()
    wind_list.wait_window() # block until window is destroyed

    # print("OK")


def btn_input_select(event):
    device_connect(f"/v2/main/prepareInputChange?input={dev_input_now.get()}")
    device_connect(f"/v2/main/setInput?input={dev_input_now.get()}")

loc_frame_row = 1
loc_frame_col = 3
frame_input = ttk.Labelframe(wind, text='Input (вход):', width=min_size_w-10)
frame_input.columnconfigure(0, minsize = (min_size_w-10)//loc_frame_col//4, weight=3)
frame_input.columnconfigure(1, minsize = (min_size_w-10)//loc_frame_col//4, weight=1)
frame_input.grid(column=0, row=level_row, sticky="nesw", padx=3)

device_parametrs = device_connect("/v2/system/getFeatures")
dev_inp_list=[]
if device_parametrs != cod_error:
    for el in device_parametrs.json()["system"]["input_list"]:
        dev_inp_list.append(el["id"])
    dev_inp_list.sort()

dev_input_now = tk.StringVar()
dev_input_now.set(dev_inp_list[0])
btn_input = ttk.Combobox(frame_input, values=dev_inp_list, textvariable=dev_input_now, state="readonly") #, width=-(min_size_w-50))
btn_input.grid(column=0, sticky="nesw", padx=3)
btn_input.bind("<<ComboboxSelected>>", btn_input_select)
btn_input_list = tk.Button(frame_input, text="выбор", command=btn_input_list_clc)
btn_input_list.grid(column=1, row=0, sticky="nesw", padx=3)

level_row += loc_frame_row

def btn_sound_program_select(event):
    global sound_program
    for el in full_program_list:
        if full_program_list[el]["pr_name"] in sound_program_now.get():
            sound_program = el
            break
    device_connect(f"/v2/main/setSoundProgram?program={sound_program}")
    btn_sound_decoder_show()


def btn_sound_decoder_show():
    if power == "on" and sound_program == "surr_decoder":
        btn_sound_decoder.config(state="readonly")
    else:
        btn_sound_decoder.config(state=tk.DISABLED)


def btn_sound_decoder_select(event):
    global sound_decoder
    for el in full_decoder_list:
        if full_decoder_list[el]["dec_name"] in sound_decoder_now.get():
            sound_decoder = el
            break
    device_connect(f"/v2/main/setSurroundDecoderType?type={sound_decoder}")


def btn_sound_program_help_clc():
    messagebox.showinfo(title=full_program_list[sound_program]["pr_name"], message=full_program_list[sound_program]["pr_info"])


def btn_sound_decoder_help_clc():
    messagebox.showinfo(title=full_decoder_list[sound_decoder]["dec_name"], message=full_decoder_list[sound_decoder]["dec_info"])

loc_frame_row = 2
loc_frame_col = 3
frame_sound_program = ttk.Labelframe(wind, text='Выбор звуковых программ', width=min_size_w-10)
frame_sound_program.grid(column=0, row=level_row, rowspan=loc_frame_row, sticky="nesw", padx=3)
frame_sound_program.columnconfigure(0, minsize = (min_size_w-10)//loc_frame_col//4, weight=3)
frame_sound_program.columnconfigure(1, minsize = (min_size_w-10)//loc_frame_col//4, weight=1)
sound_program_now = tk.StringVar()
sound_program_list = sorted([f'{el["pr_class"]} {el["pr_name"]}' for el in full_program_list.values()])
sound_program_info_text = tk.StringVar()
btn_sound_program = ttk.Combobox(frame_sound_program, values=sound_program_list, textvariable=sound_program_now,
                                 state="readonly") #, width=-(min_size_w-50))
btn_sound_program.grid(column=0, row=0, sticky="nesw", padx=3)
btn_sound_program_help =tk.Button(frame_sound_program, text="описание", command=btn_sound_program_help_clc)
btn_sound_program_help.grid(column=1, row=0, sticky="nesw", padx=3)
btn_sound_program.bind("<<ComboboxSelected>>", btn_sound_program_select)

sound_decoder_now = tk.StringVar()
btn_sound_decoder = ttk.Combobox(frame_sound_program, values=[el["dec_name"] for el in full_decoder_list.values()],
                                 textvariable=sound_decoder_now, state="readonly") #, width=-(min_size_w-50))
btn_sound_decoder.grid(column=0, row=1, sticky="nesw", padx=3)
btn_sound_decoder_help =tk.Button(frame_sound_program, text="описание", command=btn_sound_decoder_help_clc)
btn_sound_decoder_help.grid(column=1, row=1, sticky="nesw", padx=3)
btn_sound_decoder.bind("<<ComboboxSelected>>", btn_sound_decoder_select)
level_row += loc_frame_row

def btn_control_clc(btn):
    global playback
    dev_playinfo()
    if playback == "fast_reverse":
        device_connect(f"/v2/netusb/setPlayback?playback=fast_reverse_end")
        if btn == "fast_reverse_start":
            return
    elif playback == "fast_forward":
        device_connect(f"/v2/netusb/setPlayback?playback=fast_forward_end")
        if btn == "fast_forward_start":
            return
    device_connect(f"/v2/netusb/setPlayback?playback={btn}")


loc_frame_row = 2
loc_frame_col = 5
frame_control = ttk.Labelframe(wind, text='Управление', width=min_size_w-10)
frame_control.grid(column=0, row=level_row, rowspan=loc_frame_row, sticky="nesw", padx=3)
for i in range (loc_frame_col-1):
    frame_control.columnconfigure(i, minsize=(min_size_w-10)//loc_frame_col, weight=1 )
btn_control_photo_backwardend = tk.PhotoImage(file="backward_end.png")
btn_control_photo_backward = tk.PhotoImage(file="backward.png")
btn_control_photo_forwardend = tk.PhotoImage(file="forward_end.png")
btn_control_photo_forward = tk.PhotoImage(file="forward.png")
btn_control_photo_play = tk.PhotoImage(file="play.png")
btn_control_photo_pause = tk.PhotoImage(file="pause.png")
btn_control_photo_stop = tk.PhotoImage(file="stop.png")
btn_control_backwardend = tk.Button(frame_control, image=btn_control_photo_backwardend, command=lambda: btn_control_clc("previous"))
btn_control_backwardend.grid(row = 0, column = 0, sticky="nesw", padx = 3)
btn_control_play = tk.Button(frame_control, image=btn_control_photo_play, command=lambda: btn_control_clc("play"))
btn_control_play.grid(row = 0, column = 1, columnspan=2, sticky="nesw", padx = 3)
btn_control_forwardend = tk.Button(frame_control, image=btn_control_photo_forwardend, command=lambda: btn_control_clc("next"))
btn_control_forwardend.grid(row = 0, column = 3, sticky="nesw", padx=3)
btn_control_backward = tk.Button(frame_control, image=btn_control_photo_backward, command=lambda: btn_control_clc("fast_reverse_start"))
btn_control_backward.grid(row=1, column=0, sticky="nesw", padx=3)
btn_control_stop = tk.Button(frame_control, image=btn_control_photo_stop, command=lambda: btn_control_clc("stop"))
btn_control_stop.grid(row=1, column=1, sticky="nesw", padx=3)
btn_control_pause = tk.Button(frame_control, image=btn_control_photo_pause, command=lambda: btn_control_clc("pause"))
btn_control_pause.grid(row=1, column=2, sticky="nesw", padx=3)
btn_control_forward = tk.Button(frame_control, image=btn_control_photo_forward, command=lambda: btn_control_clc("fast_forward_start"))
btn_control_forward.grid(row=1, column=3, sticky="nesw", padx=3)
level_row += loc_frame_row

loc_frame_row = 10
loc_frame_col = 1
frame_info = ttk.Labelframe(wind, text='Информация:', width=min_size_w-10)
frame_info.columnconfigure(0, minsize = min_size_w-10, weight=1)
frame_info.grid(column=0, row=level_row, rowspan=loc_frame_row, sticky="nesw", padx=3)
text_info = tk.StringVar()
btn_info = tk.Label(frame_info, textvariable=text_info, justify=tk.LEFT, wraplength=min_size_w-20)
btn_info.grid(row=0, column=0, sticky="nsw", padx=3)
level_row += loc_frame_row

loc_frame_row = 1
frame_picture_play = ttk.Labelframe(wind, text="Картинка", width=min_size_w-10)
frame_picture_play.grid(column=0, row=level_row, sticky="nesw", padx=3)
frame_picture_play.columnconfigure(0, weight=1)
frame_picture_play.rowconfigure(0, weight=1)
# picture_play_pic = tk.PhotoImage()
# spisok_picture_info = tk.StringVar()
picture_play = tk.Label(frame_picture_play)
picture_play.grid(row=0, column=0, sticky="nswe", padx=3)
level_row += loc_frame_row


def btn_chk_clc():
    global chk_file
    if dev_input_now.get() in net_usb_list:
        chk_file = True

def set_dir_on_device(last_path):
    """установка на устройстве каталога, как текущего"""
    responce = device_connect("/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru")
    if responce != cod_error:
        while responce.json()['menu_layer'] != 0 and responce != cod_error:
            if device_connect("/v2/netusb/setListControl?list_id=main&type=return") == cod_error:
                return
            responce = device_connect("/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru")
    tmp_path = os.path.split(last_path)
    tmp_p_list = []
    while tmp_path[1] != "аудио" and len(tmp_path[0]) > 3:
        tmp_p_list.append(tmp_path[1])
        tmp_path = os.path.split(tmp_path[0])
    tmp_p_list.reverse()
    list_next_point = ['hms120', 'каталоги медиа-ресурсов', 'аудио'] + tmp_p_list
    for i in range(len(list_next_point)):
        index_start = 0
        max_ln = responce.json()['max_line']
        responce = cod_error
        indx_find = -1
        indx_now = 0
        attr_now = []
        while (max_ln - index_start) >= 0:
            responce = device_connect(f"/v2/netusb/getListInfo?input=server&index={index_start}&size=8&lang=ru")
            if responce != cod_error:
                for j in range(len(responce.json()["list_info"])):
                    if responce.json()["list_info"][j]['text'].lower() == list_next_point[i]:
                        indx_find = indx_now
                        attr_now = dec_in_doble(responce.json()["list_info"][j]['attribute'])
                        break
                    else:
                        indx_now += 1
            else:
                break
            if indx_find == indx_now:
                break
            index_start += 8
        if indx_find != -1 and attr_now[1] == 1:
            device_connect(f"/v2/netusb/setListControl?list_id=main&type=select&index={indx_find}")
            responce = device_connect("/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru")
        else:
            messagebox.showinfo(title="Ошибка поиска каталогов!",
                                message=f"не найдено {list_next_point[i]} в каталоге \n{last_path}")
            return


def btn_rnd_clc():
    global last_path
    if dev_input_now.get() != "server":
        messagebox.showinfo(title="Выберите server",
                            message=f"Кнопка работает только для проигрывания с сервера HMS120 и подключенного диска Z с музыкой")
        return
    list_all_dirs = []
    for dirs in dirs_w_audio:
        tmp = os.walk(os.path.normpath(dirs))
        for el in tmp:
            tmp_path = os.path.normpath(el[0])
            tmp_path = os.path.normcase(tmp_path)
            for file in el[2]:
                tmp_file = file.lower()
                if tmp_file[tmp_file.rfind("."):] in aud_files:
                    list_all_dirs.append(tmp_path)
                    break
    if len(list_all_dirs) > 0:
        last_path = choice(list_all_dirs)
        try:
            with open("play_history_dir.txt", "a", errors="replace") as file_out_dir:  # encoding="utf8"
                file_out_dir.write(datetime.datetime.now().strftime("%d-%m-%Y\t%H:%M:%S\t") + last_path + "\n")
        except PermissionError:
            messagebox.showinfo(title="Ошибка записи истории каталогов!", message=f"Закройте файл play_history_dir.txt! Каталог \n{last_path}\n не записан")
        set_dir_on_device(last_path)
        btn_input_list_clc()
    else:
        messagebox.showinfo(title="Проблемы с сервером", message="Не могу найти папку с музыкой")


def btn_lastdir_clc():
    global last_path
    if messagebox.askyesno(message=f"Последний автоматически выбранный каталог:\n{last_path}",
                            detail="\nУстановить этот каталог на устройстве как текущий?",
                            icon='question', title='Выбор каталога на устройстве'):
        if dev_input_now.get() != "server":
            messagebox.showinfo(title="Информация",
                                message=f"Установка каталога работает только для проигрывания с сервера HMS120")
            return
        set_dir_on_device(last_path)
        btn_input_list_clc()


loc_frame_row = 1
loc_frame_col = 3
frame_func = ttk.Labelframe(wind, text='Функции:', width=min_size_w-10)
for i in range(loc_frame_col):
    frame_func.columnconfigure(i, minsize = (min_size_w-10)//loc_frame_col, weight=1)
frame_func.grid(column=0, row=level_row, sticky="nesw", padx=3)
btn_chk = tk.Button(frame_func, text="Чек", command=btn_chk_clc)
btn_chk.grid(row=0, column=0, sticky="nsew", padx=3)
btn_rnd = tk.Button(frame_func, text="RndDir", command=btn_rnd_clc)
btn_rnd.grid(row=0, column=1, sticky="nsew", padx=3)
btn_lastdir = tk.Button(frame_func, text="LastDir", command=btn_lastdir_clc)
btn_lastdir.grid(row=0, column=2, sticky="nsew", padx=3)
level_row += loc_frame_row




def chk_window():
    global power, volume, volume_calc, scale_use, actual_volume, mute, dev_input_now, sound_program, sound_program_now
    global sound_decoder, sound_decoder_now
    responce = device_connect("/v2/main/getStatus")
    if responce != cod_error:
        zone_status = responce.json()
        actual_volume = zone_status["actual_volume"]
        power = zone_status["power"]
        volume = zone_status["volume"]
        mute = zone_status["mute"]
        dev_input_now.set(zone_status["input"])
        sound_program = zone_status["sound_program"]
        sound_program_now.set(f'{full_program_list[sound_program]["pr_class"]} {full_program_list[sound_program]["pr_name"]}')
        sound_program_info_text.set(full_program_list[sound_program]["pr_info"])
        sound_decoder = zone_status["surr_decoder_type"]
        sound_decoder_now.set(full_decoder_list[sound_decoder]["dec_name"])


        # pprint.pprint(zone_status)

        volume_calc = volume_min + volume * volume_step
        if scale_use:
            scale_var.set(volume_calc)
        else:
            scale_use = True
        match power:
            case "on":
                btn_power.config(image=btn_power_photo_on)
                scale_volume.config(state=tk.NORMAL)
                btn_volume_down.config(state=tk.NORMAL)
                btn_volume_up.config(state=tk.NORMAL)
                btn_volume_mute.config(state=tk.NORMAL)
                btn_input.config(state="readonly")
                btn_sound_program.config(state="readonly")
                btn_sound_decoder_show()
                btn_control_backwardend.config(state=tk.NORMAL)
                btn_control_play.config(state=tk.NORMAL)
                btn_control_forwardend.config(state=tk.NORMAL)
                btn_control_backward.config(state=tk.NORMAL)
                btn_control_stop.config(state=tk.NORMAL)
                btn_control_pause.config(state=tk.NORMAL)
                btn_control_forward.config(state=tk.NORMAL)
                # btn_input_list.config(state=tk.NORMAL)

            case "standby":
                btn_power.config(image=btn_power_photo_off)
                scale_volume.config(state=tk.DISABLED)
                btn_volume_down.config(state=tk.DISABLED)
                btn_volume_up.config(state=tk.DISABLED)
                btn_volume_mute.config(state=tk.DISABLED)
                btn_input.config(state=tk.DISABLED)
                btn_sound_program.config(state=tk.DISABLED)
                btn_sound_decoder_show()
                btn_control_backwardend.config(state=tk.DISABLED)
                btn_control_play.config(state=tk.DISABLED)
                btn_control_forwardend.config(state=tk.DISABLED)
                btn_control_backward.config(state=tk.DISABLED)
                btn_control_stop.config(state=tk.DISABLED)
                btn_control_pause.config(state=tk.DISABLED)
                btn_control_forward.config(state=tk.DISABLED)
                # btn_input_list.config(state=tk.DISABLED)
        if mute:
            btn_volume_mute.config(image=btn_volume_photo_mute_on)
        else:
            btn_volume_mute.config(image=btn_volume_photo_mute_off)
        dev_playinfo()

        # print(actual_volume, volume, zone_status['surr_decoder_type'], sep="\n")

def dev_playinfo():
    global playback, last_play, chk_file, last_play_pic
    if dev_input_now.get() in net_usb_list and power == "on":
        btn_input_list.config(state=tk.NORMAL)
        responce = device_connect("/v2/netusb/getPlayInfo")
        if responce != cod_error:
            play_info = responce.json()
            playback = play_info["playback"]
            info_str = f"Вход: {dev_input_now.get()}, состояние: {playback}\n"
            info_str += f'Артист: {play_info["artist"]}\n' if play_info["artist"] != "" else ""
            info_str += f'Альбом: {play_info["album"]}\n' if play_info["album"] != "" else ""
            info_str += f'Трек: {play_info["track"]}\n' if play_info["track"] != "" else ""
            info_str += f"Длительность: {show_time(play_info['total_time'])} " if play_info["total_time"] != 0 else ""
            info_str += f"Играет: {show_time(play_info['play_time'])}"
            text_info.set(info_str)
            albumart_url = (dev_url + play_info["albumart_url"]) if play_info["albumart_url"] != "" else ""
            if albumart_url != "" and last_play_pic != albumart_url:
                image_bite_pic = requests.get(albumart_url, timeout=10)
                # print(f"запрос {image_bite_pic.url} ответ: {image_bite_pic.status_code}")
                if image_bite_pic.status_code == 200:
                    pil_image_pic = Image.open(BytesIO(image_bite_pic.content))
                    image = ImageTk.PhotoImage(scale_image(pil_image_pic))
                    # label.config(image=image, text='')
                    # spisok_image.configure(data=image_bite.content)
                    picture_play.configure(image=image)
                    picture_play.image = image # строка чтобы картинка не улетала в мусор после завершения подпрограммы
                else:
                    picture_play.configure(image="")
            elif albumart_url == "":
                picture_play.configure(image="")
            last_play_pic = albumart_url
            now_play = f'{dev_input_now.get()}\t{play_info["artist"]}\t{play_info["album"]}\t{play_info["track"]}'
            if now_play != last_play and (now_play != "\t\t\t" or now_play != "" or last_play != ""):
                # print("смена трека ", info_str)
                try:
                    with open("play_history.txt", "a", errors="replace") as file_out: #encoding="utf8"
                        if chk_file and last_play != "":
                            last_play += "\tпроверить"
                            chk_file = False
                            file_out.write(datetime.datetime.now().strftime("%d-%m-%Y\t%H:%M:%S\t") + last_play + "\n")
                        file_out.write(datetime.datetime.now().strftime("%d-%m-%Y\t%H:%M:%S\t")+now_play+"\t\n")
                        last_play = now_play
                except PermissionError:
                    messagebox.showinfo(title="Ошибка записи истории!", message="Закройте файл play_history.txt!")
                # except UnicodeEncodeError:
    else:
        playback = "stop"
        btn_input_list.config(state=tk.DISABLED)
        text_info.set("")


            # print(info_str)



def chk_window_loop():
    chk_window()
    wind.after(5000, chk_window_loop)


chk_window_loop()


wind.mainloop()
