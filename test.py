import time
import random
import decimal
import tkinter as tk

root = tk.Tk()

randomnum = float(decimal.Decimal(random.randrange(100, 10000)) / 100)
guess = 0


def get(entry):
    guess = entry.get()
    return guess


def main():
    b1 = tk.Button(root, text="Guess", command=get)
    entry = tk.Entry()
    b1.grid(column=1, row=0)
    entry.grid(column=0, row=0)
    root.mainloop()
    print(guess)
    if guess < randomnum:
        l2 = tk.Label(root, text="Higher!")
        l2.grid(column=0, row=2)
    elif guess > randomnum:
        l3 = tk.Label(root, text="Lower!")
        l3.grid(column=0, row=2)


while guess != randomnum:
    main()
l4 = tk.Label(root, text="Well guessed")
time.sleep(10)