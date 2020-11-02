from time import sleep
from tkinter import Frame, Button, Label, Toplevel
from tkinter.ttk import Combobox
from tkinter.constants import LEFT
from controller_util import Controller, button_str_var_mapping
from PIL import Image, ImageTk
import numpy as np
from NameChangeableButton import KeyMappingButton
from mapping import mapping
from glob import glob


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
        self.mapping = mapping()
        self.pad = Controller(self.mapping, self.imLabel, record_mode=False)

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
            self.pad = Controller(self.mapping, self.imLabel, record_mode=False)
        self.pad.name = "Controller"
        self.pad.start()

    def stop(self):
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

    def confirm_setting(self, win, buttons):
        for button in buttons:
            button.configure(bg="SystemButtonFace")
        texts = [button["text"] for button in buttons]
        a = [duplicates(texts, x) for x in set(texts) if texts.count(x) > 1]
        if len(a) == 1:
            if buttons[a[0][0]]["text"] != "NONE":
                for ind in a[0]:
                    buttons[ind].configure(bg="red")
        else:
            for dup_ind_pair in a:
                if buttons[dup_ind_pair[0]]["text"] == "NONE":
                    continue
                for ind in dup_ind_pair:
                    buttons[ind].configure(bg="red")
            return

        for index, key in enumerate(self.mapping.controller_keyboard.keys()):
            self.mapping.controller_keyboard[key] = buttons[index]["text"]

        self.mapping.keyboard_controller = {
            v: k for k, v in self.mapping.controller_keyboard.items()
        }
        win.destroy()

    def check_duplicate_button(self, keys):
        a = [duplicates(keys, x) for x in set(keys) if keys.count(x) > 1]
        if len(a) == 1:
            if self.buttons[a[0][0]]["text"] != "NONE":
                for ind in a[0]:
                    self.buttons[ind].configure(bg="red")
        else:
            for dup_ind_pair in a:
                if self.buttons[dup_ind_pair[0]]["text"] == "NONE":
                    continue
                for ind in dup_ind_pair:
                    self.buttons[ind].configure(bg="red")

    def reset_button_text(self, keys):
        for button in self.buttons:
            button.configure(bg="SystemButtonFace")
        # texts = [button["text"] for button in buttons]

        for index, button in enumerate(self.buttons):
            button.configure(text=keys[index])

    def loadprofile(self):
        path = self.combox.get()
        path = "configs/" + path + ".ini"
        self.mapping.read_key_mappings(path)
        keys = list(self.mapping.controller_keyboard.values())
        self.reset_button_text(keys)

    def saveprofile(self):
        ini_name = self.combox.get()
        keys = [self.buttons[i]["text"] for i in range(26)]
        self.check_duplicate_button(keys)
        msg = ""
        for i, item in enumerate(self.mapping.controller_keyboard.items()):
            msg = msg + "{}    {}\n".format(item[0], keys[i])
        with open("configs/" + ini_name + ".ini", "w") as f:
            f.writelines(msg)

    def change_settings(self):
        win = Toplevel()
        win.lift()
        win.focus_force()
        win.grab_set()
        win.grab_release()
        dropdown_frame = Frame(win)
        dropdown_frame.pack()
        button_frame = Frame(win)
        button_frame.pack(pady=20)
        setting_frame = Frame(win)
        setting_frame.pack(pady=20)
        self.buttons = [None] * 26
        rows = 13

        self.combox = Combobox(dropdown_frame)
        self.combox.pack(side=LEFT)
        inis = glob("configs/*.ini")
        inis = [ini.split(".")[0].split("\\")[-1] for ini in inis]
        self.combox["values"] = inis

        self.loadbutton = Button(
            dropdown_frame,
            text="load",
            width=self.buttonwidth,
            command=self.loadprofile,
        )
        self.loadbutton.pack(side=LEFT)

        self.savebutton = Button(
            dropdown_frame,
            text="save",
            width=self.buttonwidth,
            command=self.saveprofile,
        )
        self.savebutton.pack(side=LEFT)
        for index, items in enumerate(self.mapping.controller_keyboard.items()):
            Label(button_frame, text=items[0], width=self.buttonwidth).grid(
                row=index % rows, column=int(index / rows) * 2
            )
            a = KeyMappingButton(button_frame, text=items[1], width=self.buttonwidth)
            if index >= 13:
                a.grid(
                    row=index % rows,
                    column=int(index / rows) * 2 + 1,
                    padx=25,
                    sticky="w",
                )
            else:
                a.grid(row=index % rows, column=int(index / rows) * 2 + 1)

            self.buttons[index] = a

        confirm_button = Button(
            setting_frame,
            text="confirm",
            width=self.buttonwidth,
            command=lambda: self.confirm_setting(win, self.buttons),
        )
        confirm_button.pack(side=LEFT)
        # save_button = Button(
        #     setting_frame,
        #     text="save",
        #     width=self.buttonwidth,
        #     command=self.save_profile,
        # )
        # save_button.pack(side=LEFT, padx=10)
        win.wm_title("Window")

    def save_profile(self):
        pass

    def on_closing(self):
        self.stop()
        self.master.quit()
        self.master.destroy()
        exit(0)


app = Application()


app.master.title("Hello")
app.mainloop()