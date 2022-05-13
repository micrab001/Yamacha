import requests
import pprint
import tkinter as tk
from tkinter import ttk
import time

root=tk.Tk()

ttk.Entry(root).grid()   # something to interact with
max_val = 100
step_cikl = 1

def dismiss ():
    dlg.grab_release()
    dlg.destroy()

def cikl():
    for i in range(0, 100, step_cikl):
        p.configure(value=i)
        time.sleep(0.5)
        p.update()
        print(i)

dlg = tk.Toplevel(root)
p = ttk.Progressbar(dlg, orient=tk.HORIZONTAL, length=200, mode='determinate', maximum=max_val, value=0)
p.grid()
ttk.Button(dlg, text="Done", command=dismiss).grid()
ttk.Button(dlg, text="Start", command=cikl).grid()
dlg.protocol("WM_DELETE_WINDOW", dismiss) # intercept close button
dlg.transient(root)   # dialog window is related to main
dlg.wait_visibility() # can't grab until window appears, so we wait
dlg.grab_set()        # ensure all input goes to our window
dlg.wait_window()     # block until window is destroyed

root.mainloop()

exit(0)

# import socket
# comp_ip = socket.gethostbyname(socket.gethostname())
# localnet = comp_ip[0:comp_ip.rfind(".")-len(comp_ip)+1]
#
# rez = []
# # rez1 = []
# for i in range(1,256):
#     net_address = f"http://{localnet}{str(i)}"
#     try:
#         responce = requests.get(net_address, timeout=(0.01, 1))
#         print(f"Получение ответа от адреса {net_address} : ", responce)
#         rez.append(f"Получен ответа от адреса {net_address}: {responce}")
#         # rez1.append(socket.gethostbyaddr(f"{localnet}{str(i)}"))
#     except requests.exceptions.ConnectionError:
#         print(f"Получение ответа от адреса {net_address} : Ошибка! Подключение не установлено")
#
# print(rez)
# print(rez1)



import json
#
link = "http://192.168.50.156/YamahaExtendedControl"
#
# # link += "/v2/system/getDeviceInfo"
# getDeviceInfo = {
#     "response_code": 0,
#     "model_name": "RX-V485",
#     "destination": "F",
#     "device_id": "F086204A289E",
#     "system_id": "084BED33",
#     "system_version": 1.78,
#     "api_version": 2.11,
#     "netmodule_generation": 2,
#     "netmodule_version": "1107    ",
#     "netmodule_checksum": "79DE0042",
#     "serial_number": "Y219680ZP",
#     "category_code": 1,
#     "operation_mode": "normal",
#     "update_error_code": "00000000",
#     "net_module_num": 1,
#     "update_data_type": 0
# }
#
# # "power": "standby"
#"/v2/main/getStatus"

# link += "/v2/main/getStatus"
# link += "/v2/main/setSleep?sleep=0"
link = link + "/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru"
# link = link + "/v2/netusb/setListControl?list_id=main&type=select&index=0"
# link += "/v2/netusb/getRecentInfo"

# "fast_reverse_start" / "fast_reverse_end" / "fast_forward_start" /
# "fast_forward_end"


responce = requests.get(link, timeout=10)
if responce.status_code == 200:
    pprint.pprint(responce.json())
else:
    print("Сбой, ответ: ", responce)


# http://{host}/YamahaExtendedControl/v1/netusb/setListControl?list_id=main&type=select&index=1

