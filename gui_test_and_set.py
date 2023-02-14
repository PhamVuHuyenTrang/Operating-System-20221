import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

import tkinter as Tk

# == CREATE PLOT ==
# create a sample DataFrame
data = {
    'thread': ['thread_0', 'thread_1', 'thread_2', 'thread_3'],
    'start_time': [0, 1, 1.5, 2.0],
    'arrival_time': [1.5, 4, 2, 6]
}
df = pd.DataFrame(data)

# calculate the duration of each thread
df['duration'] = df['arrival_time'] - df['start_time']

# set up the plot
sns.set_style('whitegrid')
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_ylim([0, len(df)])
ax.set_yticks(range(len(df)))
ax.set_yticklabels(df['thread'])
ax.set_xlim([0, 10])
ax.set_xticks([])
ax.set_xlabel('Time')
ax.set_title('')

# define a function to update the bar chart for each time step
def update_plot(frame):
    ax.clear()
    # plot the bars for each thread
    for i, row in df.iterrows():
        if frame >= row['start_time'] and frame <= row['arrival_time']:
            duration = row['arrival_time'] - row['start_time']
            progress = (frame - row['start_time']) / duration
            ax.barh(i, progress * 10, height=0.8, color=sns.color_palette("pastel")[i])
        elif frame > row['arrival_time']:
            ax.barh(i, 10, height=0.8, color=sns.color_palette("pastel")[i])
    # set the y-axis limits and labels
    ax.set_ylim([0, len(df)])
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['thread'])

    # add a y-axis on the right with "BARRIER" label
    ax2 = ax.twinx()
    ax2.set_ylim([0, len(df)])
    ax2.set_yticks([])
    ax2.set_ylabel('BARRIER', rotation=270)
    # remove the x-axis ticks and label
    ax.set_xticks([])
    ax.set_xlabel('')
    # add a title to the plot
    ax.set_title('Process synchronization (Time = {0:.2f})'.format(frame))
  
# create an animation object
ani = FuncAnimation(fig, update_plot, frames=range(7), interval=1500, repeat=True)
plt.show()

# == CREATE TKINTER WINDOW ==
# root = Tk.Tk()
# label = Tk.Label(root,text="SHM Simulation").grid(column=0, row=0)

# canvas = FigureCanvasTkAgg(fig, master=root)
# canvas.get_tk_widget().grid(column=0,row=1)


# ani = FuncAnimation(fig, update_plot, frames=range(7), interval=1500, repeat=True)


# Tk.mainloop()