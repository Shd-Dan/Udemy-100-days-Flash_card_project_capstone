from random import choice
from tkinter import *

import pandas as pnd

BACKGROUND_COLOR = "#B1DDC6"

# ----------------------------------- Reading CSV by Pandas ----------------------------------- #
current_card = {}
data_frame_dict = {}

try:
    data_frame = pnd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pnd.read_csv("data/french_words.csv")
    data_frame_dict = original_data.to_dict(orient="records")
else:
    data_frame_dict = data_frame.to_dict(orient="records")


def french_word_random():
    global current_card
    global flip_timer

    window.after_cancel(flip_timer)
    current_card = choice(data_frame_dict)
    canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    canvas.itemconfig(word_title, text="French", fill="black")
    canvas.itemconfig(card_image, image=card_front_img)
    flip_timer = window.after(3000, card_flip)


def card_flip():
    canvas.itemconfig(french_word, text=current_card["English"], fill="white")
    canvas.itemconfig(word_title, text="English", fill="white")
    canvas.itemconfig(card_image, image=card_back_img)


def is_known():
    data_frame_dict.remove(current_card)
    data = pnd.DataFrame(data_frame_dict)
    data.to_csv("data/words_to_learn.csv", index=False)

    french_word_random()


# ----------------------------------- UI ----------------------------------- #

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=card_flip)

# Front and back images
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front_img)

# Text basic configuration
word_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_button_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_button_image, highlightthickness=0, border=0, command=is_known)
right_button.grid(column=0, row=1)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, border=0, command=french_word_random)
wrong_button.grid(column=1, row=1)

french_word_random()

window.mainloop()
