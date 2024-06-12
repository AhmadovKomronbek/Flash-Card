from tkinter import *
from tkinter import messagebox
import pandas
import random

#Fileni copyalash
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError or pandas.errors.EmptyDataError:
    data_french = pandas.read_csv("data/french_words.csv")
else:
    words_list = pandas.DataFrame.to_dict(data, orient="records")

random_word = {}


def next_time():
    # jsonda jug'atlar borligini tekshirish
    global data_french
    global random_word
    global words_list
    global timer
    try:
        random_word = random.choice(words_list)
        timer = window.after(3000, change_background_image)
        window.after_cancel(timer)
        canvas.itemconfig(canvas_image, image=bg_front)
        canvas.itemconfig(title, text="French")
        canvas.itemconfig(word, text=random_word["French"])
    except IndexError:
        restart = messagebox.askyesno(title="Ex... !", message="Do yo want learn again ?")
        if restart:
            data_french = pandas.read_csv("data/french_words.csv")
            words_list = pandas.DataFrame.to_dict(data_french, orient="records")
            next_time()

def change_background_image():
    # backgroundni almashtirish
    try:
        canvas.itemconfig(canvas_image, image=bg_back)
        canvas.itemconfig(title, text="English")
        canvas.itemconfig(word, text=random_word["English"])
    except KeyError:
        return


def correct():
    # agar topilsa keyingisiga o'tish
    try:
        words_list.remove(random_word)
        next_time()
        new_data = pandas.DataFrame(words_list)
        new_data.to_csv("data/words_to_learn.csv", index=False)
    except ValueError:
        return

# Oyna yaratish
window = Tk()
window.title("Flash Cards")
window.geometry("500x400")

# background image
canvas = Canvas(width=400, height=300, bg="#B2DDC5", highlightthickness=0)

bg_front = PhotoImage(file="images/card_front.png")
bg_back = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(305, 163, image=bg_front)

canvas.grid(row=0, column=0, columnspan=2, pady=10, padx=50)
# background texts
title = canvas.create_text(200, 120, font=("arial", 25, "normal"), text="French")
word = canvas.create_text(200, 180, font=("arial", 45, "bold"), text="")

# Buttons
check_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=check_button_image, highlightthickness=0, command=correct)
right_button.grid(row=1, column=1, pady=20)

x_button_image = PhotoImage(file="images/wrong.png")
left_button = Button(image=x_button_image, highlightthickness=0, command=next_time)
left_button.grid(row=1, column=0)

# o'yinni ishga tushurish
timer = window.after(3000, change_background_image)
next_time()

window.mainloop()

