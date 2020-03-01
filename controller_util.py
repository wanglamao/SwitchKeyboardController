from pynput import keyboard
from tkinter import *
import math
import serial
from PIL import Image, ImageTk
import json
import numpy as np
import time
import threading

A_DPAD_CENTER = 0x08
A_DPAD_U = 0x00
A_DPAD_U_R = 0x01
A_DPAD_R = 0x02
A_DPAD_D_R = 0x03
A_DPAD_D = 0x04
A_DPAD_D_L = 0x05
A_DPAD_L = 0x06
A_DPAD_U_L = 0x07

# Enum DIR Values
DIR_CENTER = 0x00
DIR_U = 0x01
DIR_R = 0x02
DIR_D = 0x04
DIR_L = 0x08
DIR_U_R = DIR_U + DIR_R
DIR_D_R = DIR_D + DIR_R
DIR_U_L = DIR_U + DIR_L
DIR_D_L = DIR_D + DIR_L

BTN_NONE = 0x0000000000000000
BTN_Y = 0x0000000000000001
BTN_B = 0x0000000000000002
BTN_A = 0x0000000000000004
BTN_X = 0x0000000000000008
BTN_L = 0x0000000000000010
BTN_R = 0x0000000000000020
BTN_ZL = 0x0000000000000040
BTN_ZR = 0x0000000000000080
BTN_MINUS = 0x0000000000000100
BTN_PLUS = 0x0000000000000200
BTN_LCLICK = 0x0000000000000400
BTN_RCLICK = 0x0000000000000800
BTN_HOME = 0x0000000000001000
BTN_CAPTURE = 0x0000000000002000

DPAD_CENTER = 0x0000000000000000
DPAD_U = 0x0000000000010000
DPAD_R = 0x0000000000020000
DPAD_D = 0x0000000000040000
DPAD_L = 0x0000000000080000
DPAD_U_R = DPAD_U + DPAD_R
DPAD_D_R = DPAD_D + DPAD_R
DPAD_U_L = DPAD_U + DPAD_L
DPAD_D_L = DPAD_D + DPAD_L

LSTICK_CENTER = 0x0000000000000000
LSTICK_R = 0x00000000FF000000  # 0 (000)
LSTICK_U_R = 0x0000002DFF000000  # 45 (02D)
LSTICK_U = 0x0000005AFF000000  # 90 (05A)
LSTICK_U_L = 0x00000087FF000000  # 135 (087)
LSTICK_L = 0x000000B4FF000000  # 180 (0B4)
LSTICK_D_L = 0x000000E1FF000000  # 225 (0E1)
LSTICK_D = 0x0000010EFF000000  # 270 (10E)
LSTICK_D_R = 0x0000013BFF000000  # 315 (13B)

RSTICK_CENTER = 0x0000000000000000
RSTICK_R = 0x000FF00000000000  # 0 (000)
RSTICK_U_R = 0x02DFF00000000000  # 45 (02D)
RSTICK_U = 0x05AFF00000000000  # 90 (05A)
RSTICK_U_L = 0x087FF00000000000  # 135 (087)
RSTICK_L = 0x0B4FF00000000000  # 180 (0B4)
RSTICK_D_L = 0x0E1FF00000000000  # 225 (0E1)
RSTICK_D = 0x10EFF00000000000  # 270 (10E)
RSTICK_D_R = 0x13BFF00000000000  # 315 (13B)

NO_INPUT = BTN_NONE + DPAD_CENTER + LSTICK_CENTER + RSTICK_CENTER

# key_mappings = {
#     'w': LSTICK_U,
#     'a': LSTICK_L,
#     's': LSTICK_D,
#     'd': LSTICK_R,
#     'i': BTN_B,
#     'o': BTN_A,
#     'l': BTN_X,
#     'j': BTN_Y,
#     'p': BTN_MINUS,
#     keyboard.Key.enter: BTN_HOME,
#     keyboard.Key.space: BTN_R,
#     keyboard.Key.up: RSTICK_U,
#     keyboard.Key.down: RSTICK_D,
#     keyboard.Key.left: RSTICK_L,
#     keyboard.Key.right: RSTICK_R
# }

import json

key_mappings = {
    'w': DPAD_U,
    'a': DPAD_L,
    's': DPAD_D,
    'd': DPAD_R,
    'i': BTN_B,
    'o': BTN_A,
    'l': BTN_X,
    keyboard.Key.enter: BTN_HOME,
    keyboard.Key.space: BTN_L,
    keyboard.Key.up: RSTICK_U,
    keyboard.Key.down: RSTICK_D,
    keyboard.Key.left: RSTICK_L,
    keyboard.Key.right: RSTICK_R
}

# data = json.dumps(key_mappings)
# with open('key_mappings.json', 'w') as f:
#     json.dump(data, f)


# Compute x and y based on angle and intensity
def angle(angle, intensity):
    # y is negative because on the Y input, UP = 0 and DOWN = 255
    x = int((math.cos(math.radians(angle)) * 0x7F) * intensity / 0xFF) + 0x80
    y = -int((math.sin(math.radians(angle)) * 0x7F) * intensity / 0xFF) + 0x80
    return x, y


def lstick_angle(angle, intensity):
    return (intensity + (angle << 8)) << 24


def rstick_angle(angle, intensity):
    return (intensity + (angle << 8)) << 44


def cmd_to_packet(command):
    cmdCopy = command
    low = (cmdCopy & 0xFF)
    cmdCopy = cmdCopy >> 8
    high = (cmdCopy & 0xFF)
    cmdCopy = cmdCopy >> 8
    dpad = (cmdCopy & 0xFF)
    cmdCopy = cmdCopy >> 8
    lstick_intensity = (cmdCopy & 0xFF)
    cmdCopy = cmdCopy >> 8
    lstick_angle = (cmdCopy & 0xFFF)
    cmdCopy = cmdCopy >> 12
    rstick_intensity = (cmdCopy & 0xFF)
    cmdCopy = cmdCopy >> 8
    rstick_angle = (cmdCopy & 0xFFF)
    dpad = decrypt_dpad(dpad)
    left_x, left_y = angle(lstick_angle, lstick_intensity)
    right_x, right_y = angle(rstick_angle, rstick_intensity)

    msg = str(high)+" "+str(low)+" "+str(dpad)+" "+str(left_x) + \
        " "+str(left_y)+" "+str(right_x)+" "+str(right_y)
    return msg


# Convert DPAD value to actual DPAD value used by Switch


def decrypt_dpad(dpad):
    if dpad == DIR_U:
        dpadDecrypt = A_DPAD_U
    elif dpad == DIR_R:
        dpadDecrypt = A_DPAD_R
    elif dpad == DIR_D:
        dpadDecrypt = A_DPAD_D
    elif dpad == DIR_L:
        dpadDecrypt = A_DPAD_L
    elif dpad == DIR_U_R:
        dpadDecrypt = A_DPAD_U_R
    elif dpad == DIR_U_L:
        dpadDecrypt = A_DPAD_U_L
    elif dpad == DIR_D_R:
        dpadDecrypt = A_DPAD_D_R
    elif dpad == DIR_D_L:
        dpadDecrypt = A_DPAD_D_L
    else:
        dpadDecrypt = A_DPAD_CENTER
    return dpadDecrypt


current_pressed_key = set()


class Controller(threading.Thread):
    def __init__(self, record_mode=False):
        threading.Thread.__init__(self)
        self.threadID = "Controller"
        self.record_mode = record_mode
        # self.key_mappings = self.read_key_mappings()
        self.set_keyboard_listener()
        self.last_time = time.time()
        self.operation_list = []
        self.last_cmd = ''
        self.stop = False

    def set_keyboard_listener(self):
        print("running")
        listener = keyboard.Listener(on_press=self.on_press,
                                     on_release=self.on_release)
        listener.start()

    def on_press(self, key):

        global current_pressed_key

        try:
            key_ = key.char
        except AttributeError:
            key_ = key
        if key_ in key_mappings:
            current_pressed_key.add(key_)
            cur_cmd = cmd_to_packet(self.current2cmd())
            if self.last_cmd != cur_cmd and self.record_mode:

                f = open("operation_list.txt", "a+")
                now = time.time()
                duration = now - self.last_time
                self.last_time = now
                cur_operation = {"cmd": self.last_cmd, "duration": duration}
                self.operation_list.append(cur_operation)
                self.last_cmd = cur_cmd
                f.write('\'cmd\':' + cur_operation['cmd'] + ', \'duration\':' +
                        str(cur_operation['duration']) + '\n')
                print(cur_operation)
                f.close()

    def on_release(self, key):

        global current_pressed_key

        try:
            key_ = key.char
        except AttributeError:
            key_ = key
        if key_ in key_mappings:
            current_pressed_key.remove(key_)
            cur_cmd = cmd_to_packet(self.current2cmd())
            if self.last_cmd != cur_cmd and self.record_mode:

                f = open("operation_list.txt", "a+")
                now = time.time()
                duration = now - self.last_time
                self.last_time = now
                cur_operation = {"cmd": self.last_cmd, "duration": duration}
                self.operation_list.append(cur_operation)
                self.last_cmd = cur_cmd
                f.write('\'cmd\':' + cur_operation['cmd'] + ', \'duration\':' +
                        str(cur_operation['duration']) + '\n')
                print(cur_operation)
                f.close()
        if key == keyboard.Key.esc:
            return False

    def current2cmd(self):
        cmd = 0
        for key_ in current_pressed_key:
            cmd += key_mappings[key_]
        return cmd

    def set_record_mode(self, record_mode):
        self.record_mode = record_mode

    def run(self):
        # ser = serial.Serial("COM3", 38400)
        print("record mode: " + str(self.record_mode))
        while not self.stop:
            time.sleep(0.008)
            msg = cmd_to_packet(self.current2cmd())
            # print(msg)
            # ser.write(f'{msg}\r\n'.encode('utf-8'))


class draw_controller(threading.Thread):
    def __init__(self, imLabel):
        threading.Thread.__init__(self)
        self.threadID = "Controller"
        self.imLabel = imLabel
        self.X = np.int16(Image.open('./resource/X.tif'))
        self.Y = np.int16(Image.open('./resource/Y.tif'))
        self.A = np.int16(Image.open('./resource/A.tif'))
        self.B = np.int16(Image.open('./resource/B.tif'))
        self.HOME = np.int16(Image.open('./resource/HOME.tif'))
        self.PLUS = np.int16(Image.open('./resource/PLUS.tif'))
        self.MINUS = np.int16(Image.open('./resource/MINUS.tif'))
        self.RIGHT = np.int16(Image.open('./resource/RIGHT.tif'))
        self.DPAD_L = np.int16(Image.open('./resource/LEFT.tif'))
        self.DPAD_U = np.int16(Image.open('./resource/UP.tif'))
        self.DPAD_R = np.int16(Image.open('./resource/RIGHT.tif'))
        self.DPAD_D = np.int16(Image.open('./resource/DOWN.tif'))
        self.controller_array = np.int16(
            Image.open('./resource/pro_controller.png'))
        self.buttons_value_image = {
            BTN_A: self.A,
            BTN_B: self.B,
            BTN_X: self.X,
            BTN_Y: self.Y,
            BTN_HOME: self.HOME,
            BTN_PLUS: self.PLUS,
            BTN_MINUS: self.MINUS,
            DPAD_D: self.DPAD_D,
            DPAD_R: self.DPAD_R,
            DPAD_L: self.DPAD_L,
            DPAD_U: self.DPAD_U
        }

    def run(self):
        while True:
            # time.sleep(1)
            # print("haha")
            # self.imLabel.configure(image=self.nothing_pressed)
            # self.imLabel.image = self.nothing_pressed
            # print("haha")
            # time.sleep(1)
            # self.imLabel.configure(image=self.X_pressed)
            # self.imLabel.image = self.X_pressed
            img = self.compose_pressed_controller(
                self.get_pressed_keys_in_list())

            self.imLabel.configure(image=img)
            self.imLabel.image = img

    def get_pressed_keys_in_list(self):
        global current_pressed_key
        res = []
        for key in current_pressed_key:
            res.append(self.buttons_value_image[key_mappings[key]])
        return res

    def compose_pressed_controller(self, pressed_keys):
        mask = np.zeros((500, 500, 4))
        for key in pressed_keys:
            mask += key

        tmp = np.copy(self.controller_array)
        tmp = np.transpose(tmp, (2, 0, 1))
        tmp[3][mask[:, :, 3] == 0] = tmp[3][mask[:, :, 3] == 0] * 0.7
        tmp = np.transpose(tmp, (1, 2, 0))
        res = ImageTk.PhotoImage(Image.fromarray(tmp.astype('uint8'), 'RGBA'))
        return res
