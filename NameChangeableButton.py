from tkinter import Button, IntVar, Label, Toplevel
from pynput import keyboard


class KeyMappingButton(Button):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(command=self.change_key_mapping)

    def change_key_mapping(self):
        def onPress(key):
            try:
                newkey = key.char
            except AttributeError:
                newkey = key.name
            if newkey == "esc":
                okVar.set(1)
                return
            if newkey == "f1":
                self.configure(text="NONE")
                okVar.set(1)
                return
            self.configure(text=newkey)
            okVar.set(1)

        def onRelease(key):
            listener.stop()

        okVar = IntVar()
        win = Toplevel()
        win.lift()
        win.focus_force()
        win.grab_set()
        win.grab_release()
        Label(
            win,
            text="Press wanted Button or\nPress ESC to exit or\n Press F1 to set to none",
        ).pack()
        listener = keyboard.Listener(on_press=onPress, on_release=onRelease)
        listener.start()
        win.wait_variable(okVar)
        win.destroy()