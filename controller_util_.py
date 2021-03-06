from pynput import keyboard
from tkinter import *
import math
import serial
from PIL import Image, ImageTk
import os
import numpy as np
import time
import threading
from mapping import mapping
from pygame.time import Clock

# keyboard.KeyCode(13)

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
LSTICK_U = 0x0000000001000000  # 0 (000)
LSTICK_R = 0x0000000002000000  # 90 (05A)
LSTICK_D = 0x0000000004000000  # 180 (0B4)
LSTICK_L = 0x0000000008000000  # 270 (10E)
LSTICK_U_L = LSTICK_U + LSTICK_L  # 135 (087)
LSTICK_U_R = LSTICK_U + LSTICK_R  # 45 (02D)
LSTICK_D_L = LSTICK_D + LSTICK_L  # 225 (0E1)
LSTICK_D_R = LSTICK_D + LSTICK_R  # 315 (13B)

RSTICK_CENTER = 0x0000000000000000
RSTICK_U = 0x0000000100000000  # 0 (000)
RSTICK_R = 0x0000000200000000  # 90 (05A)
RSTICK_D = 0x0000000400000000  # 180 (0B4)
RSTICK_L = 0x0000000800000000  # 270 (10E)
RSTICK_U_L = RSTICK_U + RSTICK_L  # 135 (087)
RSTICK_U_R = RSTICK_U + RSTICK_R  # 45 (02D)
RSTICK_D_L = RSTICK_D + RSTICK_L  # 225 (0E1)
RSTICK_D_R = RSTICK_D + RSTICK_R  # 315 (13B)

"""
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
"""
NO_INPUT = BTN_NONE + DPAD_CENTER + LSTICK_CENTER + RSTICK_CENTER

# key_mappings = {
# "w": LSTICK_U,
# "a": LSTICK_L,
# "s": LSTICK_D,
# "d": LSTICK_R,
# "i": BTN_B,
# "o": BTN_A,
# "l": BTN_X,
# "j": BTN_Y,
# "p": BTN_MINUS,
# keyboard.Key.enter: BTN_HOME,
# keyboard.Key.space: BTN_R,
# keyboard.Key.up: RSTICK_U,
# keyboard.Key.down: RSTICK_D,
# keyboard.Key.left: RSTICK_L,
# keyboard.Key.right: RSTICK_R,
# }


# binded_keys = set()

button_str_var_mapping = {
    "BTN_Y": BTN_Y,
    "BTN_B": BTN_B,
    "BTN_A": BTN_A,
    "BTN_X": BTN_X,
    "BTN_L": BTN_L,
    "BTN_R": BTN_R,
    "BTN_ZL": BTN_ZL,
    "BTN_ZR": BTN_ZR,
    "BTN_MINUS": BTN_MINUS,
    "BTN_PLUS": BTN_PLUS,
    "BTN_LCLICK": BTN_LCLICK,
    "BTN_RCLICK": BTN_RCLICK,
    "BTN_HOME": BTN_HOME,
    "BTN_CAPTURE": BTN_CAPTURE,
    "DPAD_U": DPAD_U,
    "DPAD_R": DPAD_R,
    "DPAD_D": DPAD_D,
    "DPAD_L": DPAD_L,
    "LSTICK_R": LSTICK_R,  # 0 (000)
    "LSTICK_U": LSTICK_U,  # 90 (05A)
    "LSTICK_L": LSTICK_L,  # 180 (0B4)
    "LSTICK_D": LSTICK_D,  # 270 (10E)
    "RSTICK_R": RSTICK_R,  # 0 (000)
    "RSTICK_U": RSTICK_U,  # 90 (05A)
    "RSTICK_L": RSTICK_L,  # 180 ()# 180 (0B4)
    "RSTICK_D": RSTICK_D,
}

key_mappings = {
    #     # BTN_Y:None,
    #     # BTN_B:None,
    #     # BTN_A:None,
    #     # BTN_X:None,
    #     # BTN_L:None,
    #     # BTN_R:None,
    #     # BTN_ZL:None,
    #     # BTN_ZR:None,
    #     # BTN_MINUS:None,
    #     # BTN_PLUS:None,
    #     # BTN_LCLICK:None,
    #     # BTN_RCLICK:None,
    #     # BTN_HOME:None,
    #     # BTN_CAPTURE:None,
    #     # DPAD_U:None,
    #     # DPAD_R:None,
    #     # DPAD_D:None,
    #     # DPAD_L:None,
    #     # LSTICK_R:None,  # 0 (000)
    #     # LSTICK_U:None,  # 90 (05A)
    #     # LSTICK_L:None,  # 180 (0B4)
    #     # LSTICK_D:None,  # 270 (10E)
    #     # RSTICK_R:None,  # 0 (000)
    #     # RSTICK_U:None,  # 90 (05A)
    #     # RSTICK_L:None,  # 180 (0B4)
    #     # RSTICK_D:None,  # 270 (10E)
}


buttons = [
    BTN_Y,
    BTN_B,
    BTN_A,
    BTN_X,
    BTN_L,
    BTN_R,
    BTN_ZL,
    BTN_ZR,
    BTN_MINUS,
    BTN_PLUS,
    BTN_LCLICK,
    BTN_RCLICK,
    BTN_HOME,
    BTN_CAPTURE,
    DPAD_U,
    DPAD_R,
    DPAD_D,
    DPAD_L,
    LSTICK_R,  # 0 (000)
    LSTICK_U,  # 90 (05A)
    LSTICK_L,  # 180 (0B4)
    LSTICK_D,  # 270 (10E)
    RSTICK_R,  # 0 (000)
    RSTICK_U,  # 90 (05A)
    RSTICK_L,  # 180 (0B4)
    RSTICK_D,  # 270 (10E)
]


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
    low = cmdCopy & 0xFF
    cmdCopy = cmdCopy >> 8
    high = cmdCopy & 0xFF
    cmdCopy = cmdCopy >> 8
    dpad = cmdCopy & 0xFF
    cmdCopy = cmdCopy >> 8
    # lstick_intensity = cmdCopy & 0xFF
    lstick = cmdCopy & 0xFF
    cmdCopy = cmdCopy >> 8
    # lstick_angle = cmdCopy & 0xFFF
    # cmdCopy = cmdCopy >> 12
    # rstick_intensity = cmdCopy & 0xFF
    rstick = cmdCopy & 0xFF
    # cmdCopy = cmdCopy >> 8
    # rstick_angle = cmdCopy & 0xFFF
    dpad = decrypt_dpad(dpad)
    # left_x, left_y = angle(lstick_angle, lstick_intensity)
    # right_x, right_y = angle(rstick_angle, rstick_intensity)
    left_x, left_y = decrypt_simplified_stick(lstick)
    right_x, right_y = decrypt_simplified_stick(rstick)
    msg = (
        str(high)
        + " "
        + str(low)
        + " "
        + str(dpad)
        + " "
        + str(left_x)
        + " "
        + str(left_y)
        + " "
        + str(right_x)
        + " "
        + str(right_y)
    )
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


def decrypt_simplified_stick(stick):
    if stick == DIR_U:
        return 128, 1
    elif stick == DIR_R:
        return 255, 128
        # dpadDecrypt = A_DPAD_R
    elif stick == DIR_D:
        return 128, 255
        # dpadDecrypt = A_DPAD_D
    elif stick == DIR_L:
        return 1, 128
        # dpadDecrypt = A_DPAD_L
    elif stick == DIR_U_R:
        return 218, 37
        # dpadDecrypt = A_DPAD_U_R
    elif stick == DIR_U_L:
        return 37, 37
        # dpadDecrypt = A_DPAD_U_L
    elif stick == DIR_D_R:
        return 218, 218
        # dpadDecrypt = A_DPAD_D_R
    elif stick == DIR_D_L:
        return 37, 218
        # dpadDecrypt = A_DPAD_D_L
    else:
        return 128, 128
        # dpadDecrypt = A_DPAD_CENTER


class Controller(threading.Thread):
    def __init__(self, mapping: mapping, imLabel, record_mode=False):
        threading.Thread.__init__(self)
        self.threadID = "Controller"
        self.record_mode = record_mode
        self.listener = None
        self.last_time = time.time()
        self.operation_list = []
        self.last_cmd = ""
        self.isrunning = True
        self.current_pressed_key = set()
        self.drawer = draw_controller(imLabel, controller=self)
        self.drawer.name = "Draw Button pressing"
        self.mapping = mapping
        # self.drawer.start()

    def set_keyboard_listener(self):
        print("running")
        self.listener = keyboard.Listener(
            on_press=self.on_press, on_release=self.on_release
        )
        self.listener.name = "keyboard listener"
        self.listener.start()
        # self.listener.join()

    def on_press(self, key):

        # current_pressed_key, key_mappings

        try:
            key_ = key.char
        except AttributeError:
            key_ = key.name
        if key_ in self.mapping.controller_keyboard.values():
            self.current_pressed_key.add(self.mapping.keyboard_controller[key_])
            # cur_cmd = cmd_to_packet(self.current2cmd())
            # if self.last_cmd != cur_cmd and self.record_mode:

            #     f = open("operation_list.txt", "a+")
            #     now = time.time()
            #     duration = now - self.last_time
            #     self.last_time = now
            #     cur_operation = {"cmd": self.last_cmd, "duration": duration}
            #     self.operation_list.append(cur_operation)
            #     self.last_cmd = cur_cmd
            #     f.write(
            #         "'cmd':"
            #         + cur_operation["cmd"]
            #         + ", 'duration':"
            #         + str(cur_operation["duration"])
            #         + "\n"
            #     )
            #     print(cur_operation)
            #     f.close()

    def on_release(self, key):

        try:
            key_ = key.char
        except AttributeError:
            key_ = key.name
        if key_ in self.mapping.controller_keyboard.values():
            self.current_pressed_key.remove(self.mapping.keyboard_controller[key_])
            # cur_cmd = cmd_to_packet(self.current2cmd())
            # if self.last_cmd != cur_cmd and self.record_mode:

            #     f = open("operation_list.txt", "a+")
            #     now = time.time()
            #     duration = now - self.last_time
            #     self.last_time = now
            #     cur_operation = {"cmd": self.last_cmd, "duration": duration}
            #     self.operation_list.append(cur_operation)
            #     self.last_cmd = cur_cmd
            #     f.write(
            #         "'cmd':"
            #         + cur_operation["cmd"]
            #         + ", 'duration':"
            #         + str(cur_operation["duration"])
            #         + "\n"
            #     )
            #     print(cur_operation)
            #     f.close()
        if key == keyboard.Key.esc:
            return False

    def current2cmd(self):
        global button_str_var_mapping
        cmd = 0
        # sticks = [[], []]
        for key_ in self.current_pressed_key:
            cmd += button_str_var_mapping[key_]
        return cmd

    def set_record_mode(self, record_mode):
        self.record_mode = record_mode

    def run(self):
        clock = Clock()
        self.set_keyboard_listener()
        self.drawer.start()
        ser = serial.Serial("COM3", 19200)
        print("record mode: " + str(self.record_mode))
        while self.isrunning:
            clock.tick(120)
            msg = cmd_to_packet(self.current2cmd())
            # print(msg)
            ser.write(f"{msg}\r\n".encode("utf-8"))

        self.listener.stop()
        self.drawer.isrunning = False
        print("pad exit")


class draw_controller(threading.Thread):
    def __init__(self, imLabel, controller: Controller):
        threading.Thread.__init__(self)
        self.threadID = "Controller"
        self.controller = controller

        self.imLabel = imLabel
        self.isrunning = True
        self.X = np.int16(Image.open("./resource/X.tif"))
        self.Y = np.int16(Image.open("./resource/Y.tif"))
        self.A = np.int16(Image.open("./resource/a.png"))
        self.B = np.int16(Image.open("./resource/B.tif"))
        self.L = np.int16(Image.open("./resource/l.png"))
        self.ZL = np.int16(Image.open("./resource/zl.png"))
        self.R = np.int16(Image.open("./resource/r.png"))
        self.ZR = np.int16(Image.open("./resource/zr.png"))
        self.HOME = np.int16(Image.open("./resource/HOME.tif"))
        self.PLUS = np.int16(Image.open("./resource/PLUS.tif"))
        self.MINUS = np.int16(Image.open("./resource/MINUS.tif"))
        self.RIGHT = np.int16(Image.open("./resource/RIGHT.tif"))
        self.DPAD_L = np.int16(Image.open("./resource/LEFT.tif"))
        self.DPAD_U = np.int16(Image.open("./resource/UP.tif"))
        self.DPAD_R = np.int16(Image.open("./resource/RIGHT.tif"))
        self.DPAD_D = np.int16(Image.open("./resource/DOWN.tif"))
        self.controller_array = np.int16(Image.open("./resource/pro_controller.png"))
        self.buttons_value_image = {
            BTN_A: self.A,
            BTN_B: self.B,
            BTN_X: self.X,
            BTN_Y: self.Y,
            BTN_L: self.L,
            BTN_ZL: self.ZL,
            BTN_R: self.R,
            BTN_ZR: self.ZR,
            BTN_HOME: self.HOME,
            BTN_PLUS: self.PLUS,
            BTN_MINUS: self.MINUS,
            DPAD_D: self.DPAD_D,
            DPAD_R: self.DPAD_R,
            DPAD_L: self.DPAD_L,
            DPAD_U: self.DPAD_U,
        }

    def run(self):
        print("drawer running")
        while self.isrunning:
            img = self.compose_pressed_controller(self.get_pressed_keys_in_list())
            self.imLabel.configure(image=img)
            self.imLabel.image = img
        print("drawer exited")

    def get_pressed_keys_in_list(self):
        res = []
        for key in self.controller.current_pressed_key:
            try:
                res.append(self.buttons_value_image[button_str_var_mapping[key]])
            except Exception:
                pass
        return res

    def compose_pressed_controller(self, pressed_keys):
        mask = np.zeros((500, 500, 4))
        for key in pressed_keys:
            mask += key

        tmp = np.copy(self.controller_array)
        tmp = np.transpose(tmp, (2, 0, 1))
        tmp[3][mask[:, :, 3] == 0] = tmp[3][mask[:, :, 3] == 0] * 0.7
        tmp = np.transpose(tmp, (1, 2, 0))
        res = ImageTk.PhotoImage(Image.fromarray(tmp.astype("uint8"), "RGBA"))
        return res
