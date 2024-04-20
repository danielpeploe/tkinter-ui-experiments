"""
An experiment for one-dimensional pointing tasks similar to Fitts' original 1954 experiment, where users move a cursor between two 
alternating targets as quickly and accurately as possible. The interface controls the width of the targets and the distance 
between them, ensuring all combinations of distance and width are random.
"""

from tkinter import *
from tkinter.ttk import *
import random
import time

repetitions = 4
name = "name"
text_file_name = "experiment_log"

distances = [64, 128, 256, 512]
widths = [8, 16, 32]

is_right = True
is_left = False
count = 1

rect_left = None
rect_right = None

dist_width_combinations = []
combinations_index = 0

for dist in distances:
    for width in widths:
        dist_width_combinations.append((dist, width))
random.shuffle(dist_width_combinations)

# Handle rick rectangle click event
def handle_right(event):
    global rect_right, rect_left, is_right, is_left, count, combinations_index

    (current_distance, current_width) = dist_width_combinations[combinations_index]
    if combinations_index < (len(dist_width_combinations)) - 1:
        if count < repetitions:
            if is_right:
                c.itemconfigure(rect_left, fill='green')
                c.itemconfigure(rect_right, fill='blue')
                is_right = False
                is_left = True
                log_time(current_distance, current_width, count)
                count += 1
        else:
            if is_right:
                c.itemconfigure(rect_left, fill='green')
                c.itemconfigure(rect_right, fill='blue')
                is_right = False
                is_left = True
                combinations_index += 1
                log_time(current_distance, current_width, count)
                move_rectangles()
                count = 1
    else:
        if count < repetitions:
            if is_right:
                c.itemconfigure(rect_left, fill='green')
                c.itemconfigure(rect_right, fill='blue')
                is_right = False
                is_left = True
                log_time(current_distance, current_width, count)
                count += 1
        else:
            print("Finished Test")
            log_time(current_distance, current_width, count)
            master.after(0, master.destroy)

# Handle left rectangle click event
def handle_left(event):
    global rect_left, rect_right, is_left, is_right, count, combinations_index

    (current_distance, current_width) = dist_width_combinations[combinations_index]
    if combinations_index < (len(dist_width_combinations)) - 1:
        if count < repetitions:
            if is_left:
                c.itemconfigure(rect_right, fill='green')
                c.itemconfigure(rect_left, fill='blue')
                is_left = False
                is_right = True
                log_time(current_distance, current_width, count)
                count += 1
        else:
            if is_left:
                c.itemconfigure(rect_right, fill='green')
                c.itemconfigure(rect_left, fill='blue')
                is_left = False
                is_right = True
                log_time(current_distance, current_width, count)
                combinations_index += 1
                move_rectangles()
                count = 1

    else:
        if count < repetitions:
            if is_left:
                c.itemconfigure(rect_right, fill='green')
                c.itemconfigure(rect_left, fill='blue')
                is_left = False
                is_right = True
                log_time(current_distance, current_width, count)
                count += 1
        else:
            print("Finished Test")
            log_time(current_distance, current_width, count)
            master.after(0, master.destroy)

# Move rectangles to new distance a part and change width
def move_rectangles():
    global rect_left, rect_right

    (current_distance, current_width) = dist_width_combinations[combinations_index]
    c.coords(rect_left, 400 - current_width - (current_distance/2), 800, 400 - (current_distance/2), 0)
    c.coords(rect_right, 400 + (current_distance/2), 800, 400 + current_width + (current_distance/2), 0)

# Log time taken for each rectangle click
def log_time(current_distance, current_width, count):
    global name, text_file_name, start

    time_taken = (time.time() - start) * 1000
    start = time.time()
    with open(f"{text_file_name}.txt", "a") as csv_file:
        csv_file.write(f"{name} {current_distance} {current_width} {count} {time_taken:.1f}\n")

master = Tk()
c = Canvas(master, width=800, height=800)
c.pack()

(current_distance, current_width) = dist_width_combinations[0]
rect_left = c.create_rectangle(400 - current_width - (current_distance/2), 800, 400 - (current_distance/2), 0, fill="blue")
c.tag_bind(rect_left, "<ButtonPress-1>", handle_left)

rect_right = c.create_rectangle(400 + (current_distance/2), 800, 400 + current_width + (current_distance/2), 0, fill="green")
c.tag_bind(rect_right, "<ButtonPress-1>", handle_right)

start = time.time()

master.mainloop()
