from tkinter import *
from controller_util import Controller


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.pad = None

    def createWidgets(self):
        self.helloLabel = Label(self, text="sb")
        self.helloLabel.pack()
        self.quitButton = Button(self, text='quit', command=self.quit)
        self.quitButton.pack()
        self.playButton = Button(self, text='play', command=self.play)
        self.playButton.pack()
        self.change_record_mode_button = Button(
            self, text='Record', command=self.change_record_mode)
        self.change_record_mode_button.pack()

    def play(self):
        self.pad = Controller(record_mode=False)
        self.pad.start()

    def change_record_mode(self):
        print("before: " + str(self.pad.record_mode) + "\n" + "after: " +
              str(self.pad.record_mode != True))
        self.pad.set_record_mode(self.pad.record_mode != True)


app = Application()

app.master.title('Hello')

app.mainloop()