import serial
import time
from time import sleep
import re
from tqdm import tqdm
from controller_util import *

f = open('free_oneline_pokemon.txt', 'r')
lines = f.readlines()
operations_list = []
f.close()
for line in lines:
    cmd = line[line.find(':') + 1:line.find(',')]
    # print(cmd)
    duration = float(line[line.find(':', line.find('duration')) + 1:-1])
    operations_list.append({'cmd': cmd, 'duration': duration})

f = open('next_box.txt', 'r')
lines = f.readlines()
change_box_list = []
f.close()
for line in lines:
    cmd = line[line.find(':') + 1:line.find(',')]
    # print(cmd)
    duration = float(line[line.find(':', line.find('duration')) + 1:-1])
    change_box_list.append({'cmd': cmd, 'duration': duration})

ser = serial.Serial('COM3', 38400)
tmplist = []
#free pokemon
for j in tqdm(range(5)):
    for i in range(5):
        if i == 4:
            tmp_list = operations_list[:-1]
        else:
            tmp_list = operations_list
        for operation in tmp_list:
            msg = operation['cmd']
            ser.write(f'{msg}\r\n'.encode('utf-8'))
            sleep(operation['duration'])
    for operation in change_box_list:
        msg = operation['cmd']
        ser.write(f'{msg}\r\n'.encode('utf-8'))
        sleep(operation['duration'])
# lvl up
# try:
#     while True:
#         for operation in operations_list:
#             msg = operation['cmd']
#             ser.write(f'{msg}\r\n'.encode('utf-8'))
#             sleep(operation['duration'])
# except KeyboardInterrupt:
# print("exiting")
# msg = "0 8 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.12102365493774414)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.7474985122680664)
# msg = "0 4 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.10030198097229004)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(2.2908709049224854)
# msg = "0 0 8 128 1 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.23099207878112793)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.27367639541625977)
# msg = "0 4 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.11481761932373047)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.5575323104858398)
# msg = "0 4 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.10053300857543945)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(11.26662540435791)
# msg = "1 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.11900138854980469)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.442216157913208)
# msg = "0 0 8 128 1 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(1.8006880283355713)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(1.3317699432373047)
# msg = "0 0 8 128 1 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.940157413482666)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.23840808868408203)
# msg = "0 0 8 1 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
# sleep(0.3774278163909912)
# msg = "0 0 8 128 128 128 128"
# ser.write(f'{msg}\r\n'.encode('utf-8'))
