from tkinter import *
from controller_util import Controller, draw_controller
from PIL import Image, ImageTk
import numpy as np


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.pad = None
        self.launch_flag = False
        self.imLabel = None
        # self.createWidgets()

        self.playButton = Button(self, text='play', command=self.play)
        self.playButton.pack()
        self.change_record_mode_button = Button(
            self, text='Record', command=self.change_record_mode)
        self.change_record_mode_button.pack()
        # self.controller_canvas = Canvas(self, height=500, width=500)
        tmp = np.int16(Image.open('./resource/pro_controller.tif'))
        tmp[:, :, 3] = tmp[:, :, 3] * 0.7
        # tmp.putalpha(196)
        # alpha = tmp.split()[-1]
        # print(np.amax(np.int8(alpha).shape))
        # tmp = Image.open('./resource/pro_controller.tif').convert("RGBA")
        controller_pic = ImageTk.PhotoImage(
            Image.fromarray(tmp.astype('uint8'), 'RGBA'))
        self.imLabel = Label(self, image=controller_pic)
        self.imLabel.image = controller_pic
        self.imLabel.pack()
        self.draw_button_pressings(self.imLabel)

    # def createWidgets(self):

    def play(self):
        if self.launch_flag:
            self.launch_flag = False
            self.pad.stop = True
            return
        self.launch_flag = True
        self.pad = Controller(record_mode=False)
        self.pad.start()

    def change_record_mode(self):
        print("before: " + str(self.pad.record_mode) + "\n" + "after: " +
              str(self.pad.record_mode != True))
        self.pad.set_record_mode(self.pad.record_mode != True)

    def draw_button_pressings(self, imLabel):
        drawer = draw_controller(imLabel)
        drawer.start()


app = Application()


def on_closing():
    app.master.destroy()


app.master.title('Hello')
app.master.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()