import requests
import pprint


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
link += "/v2/netusb/getListInfo?input=server&index=0&size=8&lang=ru"
# link += "/v2/netusb/getRecentInfo"

# "fast_reverse_start" / "fast_reverse_end" / "fast_forward_start" /
# "fast_forward_end"

responce = requests.get(link, timeout=10)
if responce.status_code == 200:
    pprint.pprint(responce.json())
else:
    print("Сбой, ответ: ", responce)






# 125829122, 125829140, 125829124

# перевод десятичного в двоичное (вывод задом наперед)
n = int(responce.json()["list_info"][0]["attribute"])
attr_in_duble_sys = []
while n > 0:
    attr_in_duble_sys.append(n % 2)
    n = n // 2
print(attr_in_duble_sys)

# 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1
# 0 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1
# 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1

## перевод десятичного числа в двоичное
# number = int(input())
# mas_raz = []
# a = 1
# while a <= number:
#     mas_raz.append(a)
#     a *= 2
# mas_raz.reverse()
# n_bin = []
# s_tmp = 0
# i = 0
# while i < len(mas_raz):
#     if number - mas_raz[i] >= 0:
#         n_bin.append(1)
#         number -= mas_raz[i]
#     else:
#         n_bin.append(0)
#     i += 1
# print(n_bin)





# dev_inp_list=[]
# for el in responce.json()["system"]["input_list"]:
#     # dev_inp_list.append(el)
#     print(el)


# link = "http://192.168.50.156"
# responce = requests.get(link, timeout=10)
# if responce.status_code == 200:
#     # for el in responce.json()
#     print(json.dumps(responce.json(), indent= 4))
# else:
#     print("Получение списка ККТ, ответ: ", responce)
