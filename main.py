
from tkinter import *
import pandas as pd
import random


# ---------------------------- CONSTANTS ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
cnt_round = 0
words_right = []
FRENCH_WORDS = pd.read_csv('./data/french_words.csv')
chosen_word = None



# ---------------------------- FUNCTIONS ------------------------------- #
def choose_word():

    global chosen_word

    chosen_word = random.randint(0, len(FRENCH_WORDS) - 1)

    if chosen_word in words_right:
        choose_word()




def show_word():

    global cnt_round, chosen_word, flip_timer
    window.after_cancel(flip_timer)

    # if cnt_round % 2 != 0:
    choose_word()
    french_word = FRENCH_WORDS.iloc[chosen_word]['French']
    print(french_word)

    canvas.itemconfig(canvas_image, image=front_img)
    canvas.itemconfig(language, text='French')
    canvas.itemconfig(word, text=french_word)
    flip_timer = window.after(3000, show_translated_word)



def show_translated_word():

    global chosen_word

    english_word = FRENCH_WORDS.iloc[chosen_word]['English']
    print(english_word)
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(language, text='English')
    canvas.itemconfig(word, text=english_word)






def correct():

    global chosen_word

    if chosen_word in words_right:
        pass
    else:
        words_right.append(chosen_word)
    print(words_right)
    show_word()



def wrong():
    show_word()


# ---------------------------- UI ------------------------------- #

window = Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title('Flash')

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