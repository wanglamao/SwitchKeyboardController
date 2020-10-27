from time import sleep
from tkinter import Frame, Button, Label, Toplevel
from controller_util import Controller, draw_controller, key_mappings
from PIL import Image, ImageTk
import numpy as np


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        # self.drawer = None
        self.launch_flag = False
        self.imLabel = None
        self.buttonwidth = 2
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
        if self.launch_flag:
            self.launch_flag = False
            self.pad.isrunning = False
            self.playButton.configure(bg="SystemButtonFace")
            # self.drawer.isrunning = False
            return
        self.launch_flag = True
        # a = self.playButton.bg
        self.playButton.configure(bg="green")
        if self.pad is not None:
            self.pad = Controller(self.imLabel, record_mode=False)
        self.pad.name = "Controller"
        self.pad.start()

    def stop(self):
        # if self.launch_flag:
        self.launch_flag = False
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

    def change_settings(self):
        win = Toplevel()

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