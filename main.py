
from tkinter import *
import pandas as pd
import random
import json
from tkinter import messagebox

# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
cnt_round = 0
words_displayed = []
words_wrong = []
chosen_word = None
TITLE = 'Flash'
FRENCH_WORDS = {}


try:
    with open('wrong_words.csv', 'r') as f:
        FRENCH_WORDS = pd.read_csv(f)
except FileNotFoundError:
    FRENCH_WORDS = pd.read_csv('./data/french_words.csv')
    # FRENCH_WORDS = FRENCH_WORDS_SOURCE.to_dict(orient='records')



# ---------------------------- FUNCTIONS ------------------------------- #

def choose_word():

    global chosen_word

    chosen_word = random.randint(0, len(FRENCH_WORDS) - 1)

    if len(words_displayed) != len(FRENCH_WORDS):
        if chosen_word in words_displayed:
            choose_word()
        else:
            words_displayed.append(chosen_word)
    else:
            messagebox.showinfo(title=TITLE, message='No more words today!')
            end()
            window.quit()




def show_word():

    global cnt_round, chosen_word, flip_timer

    window.after_cancel(flip_timer)

    # if cnt_round % 2 != 0:
    choose_word()
    french_word = FRENCH_WORDS['French'][chosen_word]
    print(french_word)

    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(language, text='French')
    canvas.itemconfig(word, text=french_word)
    flip_timer = window.after(3000, show_translated_word)


def show_translated_word():

    global chosen_word

    english_word = FRENCH_WORDS['English'][chosen_word]
    print(english_word)
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language, text='English')
    canvas.itemconfig(word, text=english_word)


def correct():

    show_word()


def wrong():

    global chosen_word

    words_wrong.append(chosen_word)

    show_word()


def end():

    print(words_wrong)
    words_wrong_to_file = FRENCH_WORDS.iloc[words_wrong]
    print(words_wrong_to_file)

    words_wrong_to_file.to_csv('wrong_words.csv',index=False)



# ---------------------------- UI ------------------------------- #

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title(TITLE)

flip_timer = window.after(3000, show_translated_word)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas.grid(column=0,row=0, columnspan=2)

front_img = PhotoImage(file='./images/card_front.png')
back_img = PhotoImage(file='./images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=front_img)
language = canvas.create_text(400, 150, text='French', fill='black', font=('Ariel', 40, 'italic'))
word = canvas.create_text(400, 263, text='any', fill='black', font=('Ariel', 60, 'bold'))


my_image1 = PhotoImage(file="./images/right.png")
button_right = Button(image=my_image1, highlightthickness=0, justify='center', padx=50, command=correct)
button_right.grid(column=1,row=1)


my_image2 = PhotoImage(file="./images/wrong.png")
button_wrong = Button(image=my_image2, highlightthickness=0, justify='center', padx=50, command=wrong)
button_wrong.grid(column=0,row=1)

show_word()

window.mainloop()