import tkinter as tk
from tkinter import messagebox
from devicedata import full_program_list, full_decoder_list
from tkinter import ttk
import requests

import json
import pprint

cod_error = "error"
volume_max = 0
volume_min = -80.5
volume_step = 0.5
volume_calc = 0
scale_use = True # установка шкалы

def device_connect(add_link):
    """Связь с устройством, на входе часть адреса на выходе ошибка или ответ устройства"""
    global cod_error
    link = "http://192.168.50.156/YamahaExtendedControl"
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


wind = tk.Tk()
wind.title("Yamaha RX-V485")
wind_photo = tk.PhotoImage(file = "device.png")
wind.iconphoto(False, wind_photo)
min_size_w = 266
min_size_h = 450
wind.geometry(f"{min_size_w}x{min_size_h}+156+100")
wind.minsize(min_size_w, min_size_h)
wind.columnconfigure(0, minsize = min_size_w-4, weight=0)

level_row = 0

def btn_power_clc():
    print("Нажата кнопка вкл/выкл")
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
frame_power = ttk.Labelframe(wind, text='Вкл/выкл')
frame_power.grid(column=0, row=level_row, stick="nesw", padx = 3)
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
loc_frame_col = 5
frame_volume = ttk.Labelframe(wind, text='Громкость', width=min_size_w-6)
frame_volume.grid(column=0, row=level_row, rowspan=2, stick="nesw", padx=3)
for i in range (loc_frame_col-1):
    frame_volume.columnconfigure(i, minsize=(min_size_w-8)//loc_frame_col)
frame_volume.columnconfigure(i, weight=1)
scale_var = tk.DoubleVar()
scale_volume = tk.Scale(frame_volume, orient="horizontal", resolution= volume_step, from_= volume_min,
                        to=volume_max, command=scale_vollume_clc, variable=scale_var)
scale_volume.grid(row=0, column= 0, columnspan=loc_frame_col, stick="nesw")

btn_volume_photo_up = tk.PhotoImage(file="sound_up.png")
btn_volume_photo_down = tk.PhotoImage(file="sound_down.png")
btn_volume_photo_mute_off = tk.PhotoImage(file="mute.png")
btn_volume_photo_mute_on = tk.PhotoImage(file="mute_on.png")
btn_volume_down = tk.Button(frame_volume, image=btn_volume_photo_down, command=btn_volume_down_clc)
btn_volume_down.grid(row = 1, column = 0, stick="nesw",padx = 3)
btn_volume_up = tk.Button(frame_volume, image=btn_volume_photo_up, command=btn_volume_up_clc)
btn_volume_up.grid(row = 1, column = 4, stick="nes", padx = 3)
btn_volume_mute = tk.Button(frame_volume, command=btn_volume_mute_clc)
btn_volume_mute.grid(row = 1, column = 2, stick="nesw")
level_row += loc_frame_row


def btn_input_select(event):
    device_connect(f"/v2/main/prepareInputChange?input={dev_input_now.get()}")
    device_connect(f"/v2/main/setInput?input={dev_input_now.get()}")


loc_frame_row = 1
loc_frame_col = 1
frame_input = ttk.Labelframe(wind, text='Input (вход):')
frame_input.columnconfigure(0, minsize = min_size_w-100, weight=1)
frame_input.grid(column=0, row=level_row, stick="nesw", padx=3)

device_parametrs = device_connect("/v2/system/getFeatures")
if device_parametrs != cod_error:
    dev_inp_list=[]
    for el in device_parametrs.json()["system"]["input_list"]:
        dev_inp_list.append(el["id"])
    dev_inp_list.sort()

dev_input_now = tk.StringVar()
dev_input_now.set(dev_inp_list[0])
btn_input = ttk.Combobox(frame_input, values=dev_inp_list, textvariable=dev_input_now, state="readonly") #, width=-(min_size_w-50))
btn_input.grid(column=0, stick="nesw", padx=3)
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


def btn_sound_program_help_clc():
    messagebox.showinfo(title=full_program_list[sound_program]["pr_name"], message=full_program_list[sound_program]["pr_info"])

def btn_sound_decoder_help_clc():
    messagebox.showinfo(title=full_decoder_list[sound_decoder]["dec_name"], message=full_decoder_list[sound_decoder]["dec_info"])

loc_frame_row = 2
loc_frame_col = 2
frame_sound_program = ttk.Labelframe(wind, text='Выбор звуковых программ')
frame_sound_program.grid(column=0, row=level_row, stick="nesw", padx=3)
frame_sound_program.columnconfigure(0, minsize = min_size_w//4*2, weight=3)
frame_sound_program.columnconfigure(1, minsize = min_size_w//4, weight=1)
sound_program_now = tk.StringVar()
sound_program_list = sorted([f'{el["pr_class"]} {el["pr_name"]}' for el in full_program_list.values()])
sound_program_info_text = tk.StringVar()
btn_sound_program = ttk.Combobox(frame_sound_program, values=sound_program_list, textvariable=sound_program_now,
                                 state="readonly") #, width=-(min_size_w-50))
btn_sound_program.grid(column=0, row=0, stick="nesw", padx=3)
btn_sound_program_help =tk.Button(frame_sound_program, text="описание", command=btn_sound_program_help_clc)
btn_sound_program_help.grid(column=1, row=0, stick="nesw", padx=3)
btn_sound_program.bind("<<ComboboxSelected>>", btn_sound_program_select)

sound_decoder_now = tk.StringVar()
btn_sound_decoder = ttk.Combobox(frame_sound_program, values=[el["dec_name"] for el in full_decoder_list.values()],
                                 textvariable=sound_decoder_now, state="readonly") #, width=-(min_size_w-50))
btn_sound_decoder.grid(column=0, row=1, stick="nesw", padx=3)
btn_sound_decoder_help =tk.Button(frame_sound_program, text="описание", command=btn_sound_decoder_help_clc)
btn_sound_decoder_help.grid(column=1, row=1, stick="nesw", padx=3)
# btn_sound_decoder.bind("<<ComboboxSelected>>", btn_sound_program_select)



level_row += loc_frame_row


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

                # btn_sound_decoder.config(state="readonly")
            case "standby":
                btn_power.config(image=btn_power_photo_off)
                scale_volume.config(state=tk.DISABLED)
                btn_volume_down.config(state=tk.DISABLED)
                btn_volume_up.config(state=tk.DISABLED)
                btn_volume_mute.config(state=tk.DISABLED)
                btn_input.config(state=tk.DISABLED)
                btn_sound_program.config(state=tk.DISABLED)
                btn_sound_decoder_show()

                # btn_sound_decoder.config(state=tk.DISABLED)
        if mute:
            btn_volume_mute.config(image=btn_volume_photo_mute_on)
        else:
            btn_volume_mute.config(image=btn_volume_photo_mute_off)

        print(actual_volume, volume, zone_status['surr_decoder_type'], sep="\n")


def chk_window_loop():
    chk_window()
    wind.after(5000, chk_window_loop)


chk_window_loop()


wind.mainloop()
