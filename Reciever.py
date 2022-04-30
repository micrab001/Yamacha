import tkinter as tk
from tkinter import messagebox
from devicedata import full_program_list, full_decoder_list
from tkinter import ttk
import requests
import datetime

import json
import pprint

cod_error = "error"
volume_max = 0
volume_min = -80.5
volume_step = 0.5
volume_calc = 0
scale_use = True # установка шкалы
net_usb_list = ['airplay', 'mc_link', 'server', 'net_radio', 'bluetooth', 'usb']
chk_file = False
last_play = "" # сделай чтение файла, если есть

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
    s = sec % 60
    sec -= s
    m = sec // 60 % 60
    h = sec // 60 - m
    h = h // 60
    return f"{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}"


wind = tk.Tk()
wind.title("Yamaha RX-V485")
wind_photo = tk.PhotoImage(file = "device.png")
wind.iconphoto(False, wind_photo)
min_size_w = 300
min_size_h = 650
wind.geometry(f"{min_size_w}x{min_size_h}+156+100")
wind.minsize(min_size_w, min_size_h)
wind.columnconfigure(0, minsize = min_size_w-4, weight=0)

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


def btn_input_select(event):
    device_connect(f"/v2/main/prepareInputChange?input={dev_input_now.get()}")
    device_connect(f"/v2/main/setInput?input={dev_input_now.get()}")


loc_frame_row = 1
loc_frame_col = 1
frame_input = ttk.Labelframe(wind, text='Input (вход):', width=min_size_w-10)
frame_input.columnconfigure(0, minsize = min_size_w-100, weight=1)
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

def btn_chk_clc():
    global chk_file
    chk_file = True


loc_frame_row = 1
loc_frame_col = 2
frame_func = ttk.Labelframe(wind, text='Функции:', width=min_size_w-10)
frame_func.columnconfigure(0, minsize = (min_size_w-10)//loc_frame_col, weight=1)
frame_func.grid(column=0, row=level_row, sticky="nesw", padx=3)
btn_chk = tk.Button(frame_func, text="Чек", command=btn_chk_clc)
btn_chk.grid(row=0, column=0, sticky="nsw", padx=3)




def chk_window():
    # pass
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

        if mute:
            btn_volume_mute.config(image=btn_volume_photo_mute_on)
        else:
            btn_volume_mute.config(image=btn_volume_photo_mute_off)
        dev_playinfo()

        # print(actual_volume, volume, zone_status['surr_decoder_type'], sep="\n")

def dev_playinfo():
    global playback, last_play, chk_file
    if dev_input_now.get() in net_usb_list:
        responce = device_connect("/v2/netusb/getPlayInfo")
        if responce != cod_error:
            play_info = responce.json()
            playback = play_info["playback"]
            info_str = f"Вход: {dev_input_now.get()}\n"
            info_str += f'Артист: {play_info["artist"]}\n' if play_info["artist"] != "" else ""
            info_str += f'Альбом: {play_info["album"]}\n' if play_info["album"] != "" else ""
            info_str += f'Трек: {play_info["track"]}\n' if play_info["track"] != "" else ""
            info_str += f"Длительность: {show_time(play_info['total_time'])} " if play_info["total_time"] != 0 else ""
            info_str += f"Играет: {show_time(play_info['play_time'])}"
            text_info.set(info_str)
            albumart_url = (dev_url + play_info["albumart_url"]) if play_info["albumart_url"] != "" else ""
            now_play = f'{dev_input_now.get()}\t{play_info["artist"]}\t{play_info["album"]}\t{play_info["track"]}'
            if now_play != last_play:
                try:
                    with open("play_history.txt", "a") as file_out:
                        if chk_file:
                            last_play += "\tпроверить"
                            chk_file = False
                            file_out.write(datetime.datetime.now().strftime("%d-%m-%Y\t%H:%M:%S\t") + last_play + "\n")
                        file_out.write(datetime.datetime.now().strftime("%d-%m-%Y\t%H:%M:%S\t")+now_play+"\t\n")
                        last_play = now_play
                except PermissionError:
                    messagebox.showinfo(title="Ошибка записи истории!", message=f"Закройте файл play_history.txt!")


            # print(info_str)



def chk_window_loop():
    chk_window()
    wind.after(5000, chk_window_loop)


chk_window_loop()


wind.mainloop()
