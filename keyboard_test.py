"""
An experimental interface using Tkinter in Python. The interface allows users to cue target letters, advance targets on correct selection, 
log the time taken to select an item, randomize the keyboard layout, and configure the target set of characters.
"""

from tkinter import *
from tkinter.ttk import *
import random
import time

alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)

n = 6
target_letters = alphabet[:n]

# Change condition variable to 'static' to keep keyboard layout the same after each selection
condition = 'dynamic'
experiment_name = 'name'

block_max = n
block_length = len(target_letters) - 1

blocks = []
letter_index = 0
block_index = 0

# Generate blocks of shuffled letters
while n > 0:
    block = random.sample(target_letters, len(target_letters))
    blocks.append(block)
    n -= 1

# Handle key press event
def handle_key(label, char):
    global letter_index, block_index, block_max, block_length, condition
    
    # Dynamic keyboard changes after every selection regardless if it is correct or not
    if condition == 'dynamic':
        generate_keyboard()
        
    if letter_index < block_length:
        if char == label.get():
            letter_index += 1
            label.set(blocks[block_index][letter_index])
            log_time(char)
    else:
        if char == label.get():
            letter_index = 0
            block_index += 1
        
            if block_index < block_max:
                label.set(blocks[block_index][letter_index])
                log_time(char)
            else:
                label.set('All blocks completed')
                window.after(2000, window.destroy)

# Log time taken for each key press
def log_time(char):
    global block_max, start, condition, experiment_name
    
    time_taken = (time.time() - start) * 1000
    start = time.time()
    with open(f"experiment_{condition}_log.txt", "a") as csv_file:
        csv_file.write(f"{experiment_name} {condition} {char} {block_max} {time_taken:.1f}\n")

# Generate keyboard layout
def generate_keyboard():
    global alphabet, frame
    
    random.shuffle(alphabet)
    top_row = ''.join(letter for i, letter in enumerate(alphabet) if i < 10)
    mid_row = ''.join(letter for i, letter in enumerate(alphabet) if 9 < i < 19)
    bot_row = ''.join(letter for i, letter in enumerate(alphabet) if i >= 19)

        
    board = [top_row, mid_row, bot_row]
    
    for row in board:
        frame_row = Frame(frame)
        frame_row.grid(row=board.index(row), column=0, columnspan=2)
        for key in row:
            frame_button = Frame(frame_row, height=64, width=64)
            frame_button.pack_propagate(0)
            frame_button.pack(side="left")
    
            button = Button(frame_button, text=key, command=lambda k=key: handle_key(data, k))
            button.pack(fill=BOTH, expand=1)    
    
window = Tk()

data = StringVar()
data.set(blocks[0][letter_index])
label = Label(window, textvariable=data)
label.grid(row=0, column=1)

frame = Frame(window, borderwidth=3, relief=RIDGE)
frame.grid(row=1, column=0, columnspan=3)

generate_keyboard()
start = time.time()

window.mainloop()
