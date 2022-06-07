import requests
import pprint
import os
import pandas as pd
from datetime import date, timedelta


start_data_str = date.fromisoformat("2022-04-01")
start_data = date(2022, 4, 15)
end_data = date(2022, 4, 30)

calc_days = (end_data - start_data).days

end_data = end_data + timedelta(days=1)

print(calc_days)
for i in range(calc_days+1):
    day_start = start_data.strftime("%Y-%m-%d")
    day_end = (start_data + timedelta(days=1)).strftime("%Y-%m-%d")
    print(day_start, day_end)
    start_data += timedelta(days=1)

exit(0)
#
# last_path = "z:\\аhудио\\музыка\\01 неразобранное\\elton john discography\\original editions\\1984 - breaking hearts [1984 rocket 822 088-2] germany"
# i= 0
# tmp_path = os.path.split(last_path)
# tmp_p_list = []
# while tmp_path[1] != "аудио" and len(tmp_path[0]) > 3:
#     tmp_p_list.append(tmp_path[1])
#     tmp_path = os.path.split(tmp_path[0])
#     i += 1
# print(tmp_path)
# print(tmp_p_list)
# print(len(tmp_path[0]))
# exit(0)

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


# link += "/v2/main/getStatus"
# link += "/v2/main/setSleep?sleep=0"
# link = link + "/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru"
# link = link + "/v2/netusb/getListInfo?input=net_radio&index=0&size=8&lang=ru"
# link = link + "/v2/netusb/setListControl?list_id=main&type=select&index=0"
# link += "/v2/netusb/getRecentInfo"
link += "/v2/netusb/getPlayInfo"

# "fast_reverse_start" / "fast_reverse_end" / "fast_forward_start" /
# "fast_forward_end"
# ['HMS120', 'Каталоги медиа-ресурсов', 'Аудио', далее каталоги]

responce = requests.get(link, timeout=10)
if responce.status_code == 200:
    pprint.pprint(responce.json())
else:
    print("Сбой, ответ: ", responce)

# rez = responce.json()
# last_song = rez['recent_info'][0]['text']
# spisok = [ el['text'] for el in rez['recent_info'] ]
#
# try:
#     print(spisok.index(last_song))
# except ValueError:
#     print("не найдено")
#
#
# print(last_song)
# pprint.pprint(spisok)



# http://{host}/YamahaExtendedControl/v1/netusb/setListControl?list_id=main&type=select&index=1

