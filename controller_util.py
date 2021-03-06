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
from codec import *


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


# data = json.dumps(key_mappings)
# with open('key_mappings.json', 'w') as f:
#     json.dump(data, f)


def p_wait(waitTime):
    t0 = time.perf_counter()
    t1 = t0
    while t1 - t0 < waitTime:
        t1 = time.perf_counter()


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


"""
# my implementation
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
"""


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

    packet = [high, low, dpad, left_x, left_y, right_x, right_y, 0x00]
    # print (hex(command), packet, lstick_angle, lstick_intensity, rstick_angle, rstick_intensity)
    return packet


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
        self.ser = None
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

    # Discard all incoming bytes and read the last (latest) (returns int)
    def read_byte_latest(self):
        inWaiting = self.ser.in_waiting
        if inWaiting == 0:
            inWaiting = 1
        bytes_in = self.read_bytes(inWaiting)
        if len(bytes_in) != 0:
            byte_in = bytes_in[0]
        else:
            byte_in = 0
        return byte_in

    def wait_for_data(self, timeout=1.0, sleepTime=0.1):
        t0 = time.perf_counter()
        t1 = t0
        inWaiting = self.ser.in_waiting
        while (t1 - t0 < sleepTime) or (inWaiting == 0):
            time.sleep(sleepTime)
            inWaiting = self.ser.in_waiting
            t1 = time.perf_counter()

    def force_sync(self):
        # Send 9x 0xFF's to fully flush out buffer on device
        # Device will send back 0xFF (RESP_SYNC_START) when it is ready to sync
        self.write_bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

        # Wait for serial data and read the last byte sent
        self.wait_for_data()
        byte_in = self.read_byte_latest()

        # Begin sync...
        inSync = False
        if byte_in == RESP_SYNC_START:
            self.write_byte(COMMAND_SYNC_1)
            byte_in = self.read_byte()
            if byte_in == RESP_SYNC_1:
                self.write_byte(COMMAND_SYNC_2)
                byte_in = self.read_byte()
                if byte_in == RESP_SYNC_OK:
                    inSync = True
        return inSync

    def send_cmd(self, command=NO_INPUT):
        commandSuccess = self.send_packet(cmd_to_packet(command))
        return commandSuccess

    def sync(self):
        inSync = False

        # Try sending a packet
        inSync = self.send_packet()
        if not inSync:
            # Not in sync: force resync and send a packet
            inSync = self.force_sync()
            if inSync:
                inSync = self.send_packet()
        return inSync

    def crc8_ccitt(self, old_crc, new_data):
        data = old_crc ^ new_data

        for i in range(8):
            if (data & 0x80) != 0:
                data = data << 1
                data = data ^ 0x07
            else:
                data = data << 1
            data = data & 0xFF
        return data

    def write_bytes(self, bytes_out):
        self.ser.write(bytearray(bytes_out))
        return

    # Write byte to the serial port
    def write_byte(self, byte_out):
        self.write_bytes([byte_out])
        return

    def read_bytes(self, size):
        bytes_in = self.ser.read(size)
        return list(bytes_in)

    # Read 1 byte from the serial port (returns int)
    def read_byte(self):
        bytes_in = self.read_bytes(1)
        if len(bytes_in) != 0:
            byte_in = bytes_in[0]
        else:
            byte_in = 0
        return byte_in

    def send_packet(
        self, packet=[0x00, 0x00, 0x08, 0x80, 0x80, 0x80, 0x80, 0x00], debug=False
    ):
        if not debug:
            bytes_out = []
            bytes_out.extend(packet)

            # Compute CRC
            crc = 0
            for d in packet:
                crc = self.crc8_ccitt(crc, d)
            bytes_out.append(crc)
            self.write_bytes(bytes_out)
            # print(bytes_out)

            # Wait for USB ACK or UPDATE NACK
            byte_in = self.read_byte()
            commandSuccess = byte_in == RESP_USB_ACK
        else:
            commandSuccess = True
        return commandSuccess

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
        self.ser = serial.Serial("COM3", 19200, timeout=1)
        if not self.sync():
            print("Could not sync!")
            self.ser.close()
            return

        if not self.send_cmd(BTN_A + DPAD_U_R + LSTICK_U + RSTICK_D_L):
            print("Packet Error!")
            self.ser.close()
            return

        p_wait(0.05)

        if not self.send_cmd():
            print("Packet Error!")
            self.ser.close()
            return

        print("record mode: " + str(self.record_mode))
        while self.isrunning:
            clock.tick(120)
            self.send_packet(cmd_to_packet(self.current2cmd()))
            # print(msg)
            # ser.write(f"{msg}\r\n".encode("utf-8"))
        self.ser.close()
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
