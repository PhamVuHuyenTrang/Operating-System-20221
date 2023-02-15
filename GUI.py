# for macOS
from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")

# import libraries
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

# import modules
from run_algorithm import *


# create a sample DataFrame
data = {
    'thread': ['thread_0', 'thread_1', 'thread_2', 'thread_3'],
    'start_time': [0, 1, 1.5, 2.0],
    'arrival_time': [1.5, 4, 2, 6]
}
df = pd.DataFrame(data)

# calculate the duration of each thread
df['duration'] = df['arrival_time'] - df['start_time']

# == CREATE PLOT ==
# set up the plot with seaborn
sns.set_style('whitegrid')
sns.set_palette('deep')
fig, ax = plt.subplots()
ax.set_ylim([0, len(df)])
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['thread'])
ax.set_xlim([0, 10])
ax.set_xticks([])
ax.set_xlabel('Progress')
ax.set_title('')

# define a function to update the bar chart for each time step
def update_plot(frame):
    ax.clear()
    # plot the bars for each thread
    for i, row in df.iterrows():
        if frame >= row['start_time'] and frame <= row['arrival_time']:
            duration = row['arrival_time'] - row['start_time']
            progress = (frame - row['start_time']) / duration
            ax.barh(i, progress * 10, height=0.8, color=sns.color_palette()[i])
        elif frame > row['arrival_time']:
            ax.barh(i, 10, height=0.8, color=sns.color_palette()[i])
    # set the y-axis limits and labels
    ax.set_ylim([0, len(df)])
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['thread'])
    # remove the x-axis ticks and label
    ax.set_xticks([])
    ax.set_xlabel('')

    # add a y-axis on the right with "BARRIER" label
    ax2 = ax.twinx()
    ax2.set_ylim([0, len(df)])
    ax2.set_yticks([])
    ax2.set_ylabel('BARRIER', rotation=270)
    ax2.yaxis.set_label_coords(1.05, 0.5)

    # add a title to the plot
    ax.set_title('Process synchronization using barrier (Progress = {} seconds)'.format(frame))
    # update the text field on the tkinter frame
    # text_field.config(text='')
    for i, row in df.iterrows():
        if frame == row['start_time']:
            start_text = 'Thread {} started at: {} seconds'.format(row['thread'], row['start_time'])
            text_field.config(text=text_field.cget('text') + '\n' + start_text)
        if frame == row['arrival_time']:
            arrival_text = "Thread {} arrived at the barrier at: {} seconds".format(row['thread'], row['arrival_time'])
            text_field.config(text=text_field.cget('text') + '\n' + arrival_text)


# == CREATE GUI ==
# create a tkinter window and frame
root = tk.Tk()
root.geometry('1000x800')

# Define the 2x2 grid layout
root.columnconfigure([0, 1], weight=1)
root.rowconfigure([0, 1], weight=1)

# create frames
frame1 = tk.Frame(root, bg="white", height=600, width=500)
frame1.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

frame2 = tk.Frame(root, bg="white", height=600, width=100)
frame2.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

frame3 = tk.Frame(root, bg="white", height=100, width=500)
frame3.grid(row=1, column=0, padx=5, pady=5, sticky="nsew", columnspan=2)

# add the matplotlib plot to the tkinter frame
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')


# add a text field to the right of the plot
text_field = tk.Label(frame2, font=('Helvetica', 16))
# text_field.place(anchor="w")
text_field.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# create an animation object
ani = FuncAnimation(fig, update_plot, frames=range(7), interval=2000, repeat=False)

# buttons
# define a list of tuples for each button
button_data = [("Centralized Algorithm", run_centralized),
               ("Semaphore Algorithm", run_semaphore),
               ("Test-and-Set Algorithm", run_test_and_set),
               ("Tree-based Algorithm", run_tree_based)]

# loop through the button_data and create a button for each item
for i, (text, function) in enumerate(button_data):
    button = tk.Button(frame3, text=text, command=function, font=("Helvetica", 16))
    button.grid(row=0, column=i, padx=10, pady=10)

# center the buttons vertically and horizontally
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_columnconfigure([0, 1, 2, 3], weight=1)

# start the tkinter event loop
root.mainloop()
