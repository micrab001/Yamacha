import requests
import pprint

import os
import tkinter
from tkinter import ttk



class FoundAllFiles():



    f_loc = r'C:\Users\micrab\AppData\Local\Temp\gen_py'
    all_dir = os.listdir(f_loc)
    if len(all_dir) != 0:
        for f in all_dir:
            if os.path.isfile(f_loc+chr(92)+f):
                os.remove(f_loc+chr(92)+f)
            else:
                rmtree(f_loc+chr(92)+f)










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

