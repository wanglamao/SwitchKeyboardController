from time import sleep
from tkinter import Frame, Button, Label, Toplevel
from pynput import keyboard
from tkinter import IntVar
from controller_util import Controller, button_str_var_mapping
from PIL import Image, ImageTk
import numpy as np
from NameChangeableButton import KeyMappingButton


def duplicates(lst, item):
    return [i for i, x in enumerate(lst) if x == item]


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # self.drawer = None
        self.isOn = False
        self.imLabel = None
        self.buttonwidth = 20
        # self.createWidgets()

        self.playButton = Button(
            self, text="play", command=self.play, width=self.buttonwidth
        )
        self.playButton.grid(row=0, column=0)
        self.change_record_mode_button = Button(
            self, text="Record", command=self.change_record_mode, width=self.buttonwidth
        )
        self.change_record_mode_button.grid(row=0, column=1)
        self.settings_button = Button(
            self, text="Settings", command=self.change_settings, width=self.buttonwidth
        )
        self.settings_button.grid(row=0, column=2)
        # self.controller_canvas = Canvas(self, height=500, width=500)
        tmp = np.int16(Image.open("./resource/pro_controller.tif"))
        tmp[:, :, 3] = tmp[:, :, 3] * 0.7
        # tmp.putalpha(196)
        # alpha = tmp.split()[-1]
        # print(np.amax(np.int8(alpha).shape))
        # tmp = Image.open('./resource/pro_controller.tif').convert("RGBA")
        controller_pic = ImageTk.PhotoImage(
            Image.fromarray(tmp.astype("uint8"), "RGBA")
        )
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.imLabel = Label(self, image=controller_pic)
        self.imLabel.image = controller_pic
        self.imLabel.grid(row=1, column=0, columnspan=3)

        self.pad = Controller(self.imLabel, record_mode=False)

        # self.draw_button_pressings(self.imLabel)

    # def createWidgets(self):

    def play(self):
        if self.isOn:
            self.isOn = False
            self.pad.isrunning = False
            self.playButton.configure(bg="SystemButtonFace")
            # self.drawer.isrunning = False
            return
        self.isOn = True
        # a = self.playButton.bg
        self.playButton.configure(bg="green")
        if self.pad is not None:
            self.pad = Controller(self.imLabel, record_mode=False)
        self.pad.name = "Controller"
        self.pad.start()

    def stop(self):
        # if self.launch_flag:
        self.isOn = False
        self.pad.isrunning = False

    def change_record_mode(self):
        print(
            "before: "
            + str(self.pad.record_mode)
            + "\n"
            + "after: "
            + str(self.pad.record_mode != True)
        )
        self.pad.set_record_mode(self.pad.record_mode != True)

        # print(newkey)
        # pass

    def confirm_setting(self, win, buttons):
        for button in buttons:
            button.configure(bg="SystemButtonFace")
        texts = [button["text"] for button in buttons]
        a = [duplicates(texts, x) for x in set(texts) if texts.count(x) > 1]
        if len(a) == 1:
            if buttons[a[0][0]]["text"] != "none":
                for ind in a[0]:
                    buttons[ind].configure(bg="red")
        else:
            for dup_ind_pair in a:
                if buttons[dup_ind_pair[0]]["text"] == "none":
                    continue
                for ind in dup_ind_pair:
                    buttons[ind].configure(bg="red")
            return

        for index, key in enumerate(self.pad.controller_keyboard.keys()):
            self.pad.controller_keyboard[key] = buttons[index]["text"]

        self.pad.keyboard_controller = {
            v: k for k, v in self.pad.controller_keyboard.items()
        }
        win.destroy()

    def change_settings(self):
        # if self.isOn:
        #     self.play()
        win = Toplevel()
        win.lift()
        win.focus_force()
        win.grab_set()
        win.grab_release()
        button_frame = Frame(win)
        button_frame.pack()
        setting_frame = Frame(win)
        setting_frame.pack()
        self.buttons = [None] * 26
        rows = 13
        for index, items in enumerate(self.pad.controller_keyboard.items()):
            Label(button_frame, text=items[0], width=self.buttonwidth).grid(
                row=index % rows, column=int(index / rows) * 2
            )
            a = KeyMappingButton(button_frame, text=items[1], width=self.buttonwidth)
            a.grid(row=index % rows, column=int(index / rows) * 2 + 1)
            self.buttons[index] = a

        confirm_button = Button(
            setting_frame,
            text="confirm",
            width=self.buttonwidth,
            command=lambda: self.confirm_setting(win, self.buttons),
        )
        confirm_button.grid(row=13, column=1)
        win.wm_title("Window")

    # def draw_button_pressings(self, imLabel):
    #     self.drawer = draw_controller(imLabel, self.pad)
    #     self.drawer.name = "Draw Button pressing"
    #     self.drawer.start()

    def on_closing(self):
        # self.drawer.isrunning = False
        self.stop()
        # sleep(2)
        self.master.quit()
        self.master.destroy()
        exit(0)


app = Application()


app.master.title("Hello")
app.mainloop()