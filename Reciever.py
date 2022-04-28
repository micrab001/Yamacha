import tkinter as tk
from tkinter import ttk
import requests
import json

import pprint

cod_error = "error"
# min 0, max 161, st 1   =act_vol-min/0.5
volume_max = 0
volume_min = -80.5
volume_step = 0.5
volume_calc = 0
scale_use = True # установка шкалы

def device_connect(add_link):
    global cod_error
    link = "http://192.168.50.156/YamahaExtendedControl"
    link = link + add_link
    responce = requests.get(link, timeout=10)
    if responce.status_code == 200:
        if responce.json()["response_code"] != 0:
            print("Ошибка команды, ответ: ", responce.json()["response_code"])
            return cod_error
        else:
            return responce
    else:
        print(f"Ошибка в ответе на {add_link} от устройства, ответ: {responce}")
        return cod_error


wind = tk.Tk()
wind.title("Yamaha RX-V485")
wind_photo = tk.PhotoImage(file = "device.png")
wind.iconphoto(False, wind_photo)
wind.geometry("262x200+156+156")
min_size_w = 266
wind.minsize(min_size_w, 200)
wind.columnconfigure(0, minsize = min_size_w-6, weight=0)

level_row = 0

def btn_power_clc():
    print("Нажата кнопка вкл/выкл")
    chk_window()
    match power:
        case "on":
            print("Послать код выключить")
            device_connect("/v2/main/setPower?power=standby")
        case "standby":
            print("Послать код включить")
            device_connect("/v2/main/setPower?power=on")
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
    print("Послать значение громкости", volume_calc_set)
    print("значение переменной", scale_var.get())

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
frame_volume = ttk.Labelframe(wind, text='Громкость')
frame_volume.grid(column=0, row=level_row, rowspan=2, stick="nesw", padx=3)
for i in range (loc_frame_col-1):
    frame_volume.columnconfigure(i, minsize=(min_size_w-6)//loc_frame_col)
print("i =", i)
# frame_volume.rowconfigure(0, weight=1)
scale_var = tk.DoubleVar()
scale_volume = tk.Scale(frame_volume, orient="horizontal", resolution= volume_step, from_= volume_min, to=volume_max, command=scale_vollume_clc, variable=scale_var)
scale_volume.grid(row=0, column= 0, columnspan=loc_frame_col, stick="nesw")

btn_volume_photo_up = tk.PhotoImage(file="sound_up.png")
btn_volume_photo_down = tk.PhotoImage(file="sound_down.png")
btn_volume_photo_mute_off = tk.PhotoImage(file="mute.png")
btn_volume_photo_mute_on = tk.PhotoImage(file="mute_on.png")
btn_volume_down = tk.Button(frame_volume, image=btn_volume_photo_down, command=btn_volume_down_clc)
btn_volume_down.grid(row = 1, column = 0, stick="nesw",padx = 3)
btn_volume_up = tk.Button(frame_volume, image=btn_volume_photo_up, command=btn_volume_up_clc)
btn_volume_up.grid(row = 1, column = 4, stick="nesw", padx = 3)
btn_volume_mute = tk.Button(frame_volume, command=btn_volume_mute_clc)
btn_volume_mute.grid(row = 1, column = 2, stick="nesw")
level_row += loc_frame_row

loc_frame_row = 1
loc_frame_col = 1
frame_input = ttk.Labelframe(wind, text='Input (вход):', width=1)
frame_input.grid(column=0, row=level_row, stick="nesw", padx=3)


# btn_input = ttk.(frame_input, text="test button")
# btn_test.grid(column=0)

level_row += loc_frame_row


def chk_window():
    global power, volume, volume_calc, scale_use, actual_volume, mute
    responce = device_connect("/v2/main/getStatus")
    if responce != cod_error:
        zone_status = responce.json()
        actual_volume = zone_status["actual_volume"]
        power = zone_status["power"]
        volume = zone_status["volume"]
        mute = zone_status["mute"]

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
            case "standby":
                btn_power.config(image=btn_power_photo_off)
                scale_volume.config(state=tk.DISABLED)
                btn_volume_down.config(state=tk.DISABLED)
                btn_volume_up.config(state=tk.DISABLED)
                btn_volume_mute.config(state=tk.DISABLED)
        if mute:
            btn_volume_mute.config(image=btn_volume_photo_mute_on)
        else:
            btn_volume_mute.config(image=btn_volume_photo_mute_off)

        print(actual_volume, volume, sep="\n")


def chk_window_loop():
    chk_window()
    wind.after(5000, chk_window_loop)


chk_window_loop()


wind.mainloop()
