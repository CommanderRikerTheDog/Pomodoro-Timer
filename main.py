import tkinter
from tkinter import *
from PIL import Image, ImageTk
import math
import pygame


# ---------------------------- RESOURCES ------------------------------- #
"""I found this site to be super useful
https://tkdocs.com/tutorial/firstexample.html#walkthrough
https://pillow.readthedocs.io/en/stable/handbook/tutorial.html#using-the-image-class
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/canvas.html
https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/images.html
https://pillow.readthedocs.io/en/stable/reference/Image.html
https://www.geeksforgeeks.org/how-to-play-sounds-in-python-with-tkinter/#:~:text=There%20are%20two%20modules%20to,function%20name%20is%20playsound()
https://www.zedge.net/ringtone/6be5334d-ec22-4681-bd0e-88a51f9e8187
"""


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#47ab94"
YELLOW = "#FFF4CF"
FONT_NAME = "Courier"

REPS = 0 #starts out at 0
WORK_MIN = 0.2
SHORT_BREAK_MIN = 0.1
LONG_BREAK_MIN = 20

# This is a locally used variable, but we need to tap into it for multiple methods, so we're pulling it out as a
# global variable in order to tap into it.
timer = None

# ---------------------------- TIMER RESET ------------------------------- #

"""What we need to cancel is the window.after method which is saved in a timer= variable.
We will cancel that very thing by plugging in timer= to window.after_cancel() which is the method to cancel that
very thing. 
"""
def reset_timer():
    # Cancel the actual timer that's running
    window.after_cancel(timer)
    # Reset the timer_text that is set within canvas
    canvas.itemconfig(timer_text, text="00:00")
    # Reset the timer label
    timer_title.config(text="Timer", bg=YELLOW, font=(FONT_NAME, 45, "bold"), fg=GREEN)
    # Reset check marks
    checkmark.config(text="")
    # Set Global REPS to 0; otherwise, hitting reset will add on to previous session's checkmarks
    global REPS
    REPS = 0



# ---------------------------- TIMER PAUSE ------------------------------- #

def pause_timer():
    pass


# ---------------------------- TIMER MECHANISM ------------------------------- #

# This simply starts the countdown() function by calling upon itself (start_timer) is called upon.
# You will put this into the start_button.config command.
# Do so WITHOUT PARANTHESIS! Otherwise it just starts up automatically without being clicked on.
def start_timer():
    """Typing in global will indicate you're using a global variable"""

    global REPS
    REPS += 1 # starts out at first rep

    """Breaking out the minutes to seconds"""
    work_sec = int(WORK_MIN * 60)
    short_break_sec = int(SHORT_BREAK_MIN * 60)
    long_break_sec = int(LONG_BREAK_MIN * 60)


    """Indicating which rep is a WORK vs. S.BREAK vs. L.BREAK"""
    """This section of if/else alone will not start the timer again."""
    """We will add an else statement in the countdown method to keep looping without using a while loop"""

    # 8th REPS is a long break (4 work and 3 break sessions would have occurred by then)
    if REPS == 3:
        timer_title.config(text="Long Break", fg=PINK, font=(FONT_NAME, 45))
        countdown(long_break_sec)
        play_long_break()
    # REPS that are even number but not 8 are short breaks
    elif REPS % 2 == 0:
        timer_title.config(text="Short Break", fg=PINK, font=(FONT_NAME, 45))
        countdown(short_break_sec)
        play_short_break()
    # REPS 1, 3, 5, 7 are Work Times
    else:
        timer_title.config(text="Focus Time", fg=GREEN, font=(FONT_NAME, 45))
        countdown(work_sec)
        play_focus()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
""" EVENT-DRIVEN:
We can't use the time's countdown mechanism in Tkinter because it requires a while loop. 
This interferes with GUI programs because GUIs require a mainloop to "keep watch" of a screen, meaning
these are Event Driven. Any other loop will break that. 

We'll use window.after() method from tkinter to tell it to:
- wait one second
- a function to call after 1000 milliseconds
"""

def countdown(count):

    """
    DISPLAYING MM:SS
    # The count itself counts from seconds
    # But we don't want the timer to count simply from seconds. We want a mm:ss time clock format.
    # We'll want minutes to be divided by 60, but rounded down to show the minutes left
    """
    count_min = math.floor(count / 60)
    # Modulo % to give us the remainder of seconds by dividing all the seconds by 60
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f"0{count_sec}" #This blows my mind

    """
    HOW TO UPDATE CANVAS TEXT
    # tkinter's .after() causes a delay before something starts. 
    # 1000 milliseconds is 1 second
    # print(count) # Use this to "catch" the count and make it show up in the run area as a test!
    # Because we want to "catch" this count down and make it visible in the GUI, we will update the Canvas-Text
    

    # When Testing: Maker sure the countdown() method is called below the timer_text variable.
    # Once this runs as expected, we'll want this to be tied to a start-event, not just run automatically.
    # Hence, the "start_timer" method we will need to create, above this very function.
    """

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > -1: # prevents count down to negative
        global timer
        timer = window.after(1000, countdown, count-1)
    else:
        start_timer()
        marks = ""
        work_sessions = math.floor(REPS/2)
        for _ in range(work_sessions):
            marks += "💚"
        checkmark.config(text=marks)


# ---------------------------- BREAK SOUND ------------------------------- #

# initializes pygame
pygame.mixer.init()

def play_focus():
    pygame.mixer.music.load("ffvii_goodnight.mp3")
    pygame.mixer.music.play(loops=0)

def play_short_break():
    pygame.mixer.music.load("ffvii_victory_fanfare.mp3")
    pygame.mixer.music.play(loops=0)

def play_long_break():
    pygame.mixer.music.load("ffvii_prelude.mp3")
    pygame.mixer.music.play(loops=0)

# ---------------------------- UI SETUP ------------------------------- #

"""This is the main application window."""
window = Tk()
window.title("Pomodoro Timer")
window.config(padx=100, pady=50, bg=YELLOW)
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)

"""
CREATE A CANVAS OBJECT
You need to use Canvas if you want to overlay text on top of an image. 
Image will be a tomato; the text on top of that will be the time clock. 
"""
canvas = Canvas(width=300, height=400, bg=YELLOW, highlightthickness=0)
canvas.grid(column=1, row=2)

"""
WORKING WITH IMAGES

This is where the PIL was needed. This library was tricky to install.
1. From terminal: pip install pillow
2. To tap into the library, you use PIL

Opening & Resizing takes multiple steps:
1. Open with Image.open(filenamehere)
2. Create resize variable containing the width & height parameters as a tuple; I used floor division for simplicity. 
3. Use the .resize() method from the Image class, then feed in the resize tuple from #2.
4. Convert #3 to an ImageTk object in order to use that on the canvas later. 

"""
original_image = Image.open("tomato.png")
resize_param = (width, height) = (original_image.width // 6, original_image.height // 6)
resized_image = original_image.resize(resize_param)
final_tomato_image = ImageTk.PhotoImage(resized_image)


# Bring up the tomato image in Canvas
canvas.create_image(150, 200, image=final_tomato_image) #this is where it places the "center" of the image.

# Timer Counter in Tomato
timer_text = canvas.create_text(150, 200, text="00:00", font=(FONT_NAME, 33, "bold"), fill="#FFFFFF")



#---------------------------- TIMER TITLE LABEL ---------------------------- #
"""
Notice that the title is set up with Label class and thus is independent of the Canvas.
This means the label will not simply show up via the set up.
You need the .grid method from the Label class and actually place it somewhere.  
"""

timer_title = Label(window, text="Timer", bg=YELLOW, font=(FONT_NAME, 45, "bold"), fg=GREEN)
timer_title.grid(column=1, row=0)


#---------------------------- BUTTONS ---------------------------- #

"""Start Button"""
start_button = Button(window, text="Start", font=(FONT_NAME, 25), highlightthickness=0, bd=0, fg=GREEN,
                      command=start_timer)
start_button.grid(column=0, row=4)

"""Reset Button"""
reset_button = Button(window, text="Reset", font=(FONT_NAME, 25), highlightthickness=0, fg=GREEN, bd=0, command=reset_timer)
reset_button.grid(column=2, row=4)

"""TBD: Pause Button"""
# pause_button = Button(window, text="Pause", font=(FONT_NAME, 25), highlightthickness=0, fg=GREEN, bd=0, comman=pause_timer)
# pause_button.grid(column=1, row=4)

"""Include text="💚" after work sesh complete"""
checkmark = Label(window,  highlightthickness=0, background=YELLOW)
checkmark.grid(column=1,  row=3, pady=30)





window.mainloop()
