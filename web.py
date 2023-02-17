# streamlit tools
import streamlit as st
import streamlit.components.v1 as components

# libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.animation import FuncAnimation
import time

# utils
from run_algorithm import run

# algorithms
from Semaphore_based_barrier import main_semaphore 
from test_and_set import run_test_and_set

st.write("# Barrier Synchronization Implementations")

threads_num = st.number_input("**Number of threads/process**", 0, 32)

implementation = st.radio("**Implementation**", ('Centralized Barrier', 'Combining Tree Barrier', 'Test and Set Barrier', 'Semaphore Barrier'))


if implementation == 'Semaphore Barrier':
    algorithm = 'semaphore'
elif implementation == 'Centralized Barrier':
    algorithm = 'semaphore'
elif implementation == 'Combining Tree Barrier':
    algorithm = 'semaphore'
elif implementation == 'Test and Set Barrier':
    algorithm = 'test_and_set'

def create_file(implementation):
    if implementation == 'Semaphore Barrier':
        main_semaphore(threads_num)
    elif implementation == 'Centralized Barrier':
        main_semaphore(threads_num)
    elif implementation == 'Combining Tree Barrier':
        main_semaphore(threads_num)
    elif implementation == 'Test and Set Barrier':
        run_test_and_set(threads_num)

def handle():
    return run(algorithm)

# define a function to update the bar chart for each time step
def update_plot(frame):
    ax.clear()
    # plot the bars for each thread
    for i, row in df.iterrows():
        if frame >= row['start_time'] and frame <= row['arrival_time']:
            duration = row['arrival_time'] + 1e-6 - row['start_time']
            progress = (frame - row['start_time']) / duration
            ax.barh(i, progress * 10, height=0.8, color=sns.color_palette("pastel")[i % 10])
        elif frame > row['arrival_time']:
            ax.barh(i, 10, height=0.8, color=sns.color_palette("pastel")[i % 10])
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

    for i, row in df.iterrows():
        if frame == row['start_time']:
            start_text = '- **{}** :blue[started] at: **:blue[{}]** seconds'.format(row['thread'], row['start_time'])
            text.append(start_text)
        if frame == row['arrival_time']:
            arrival_text = "- **{}** :red[arrived] at the barrier at: **:red[{}]** seconds".format(row['thread'], row['arrival_time'])
            text.append(arrival_text)

col1, col2, col3 = st.columns(3)
start_button = col2.button('Start')
create_button = col1.button("Create demonstration")

def check_num_files():
    folder_path = './' + algorithm

    # Get a list of all the files in the folder
    files = os.listdir(folder_path)
    # Count the number of files
    num_files = len(files)
    return num_files

if create_button:
    try:
        # Remove the previous created files
        folder_path = './' + algorithm
        # Get a list of all the files in the folder
        files = os.listdir(folder_path)
        # Loop through the list and delete each file
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
        os.remove(algorithm+'.csv')
    except:
        print("No files found")

    create_file(implementation)

    # Create a spinner while waiting for files
    with st.spinner("Demonstration loading..."):
        while True:
            num_files = check_num_files()
            if num_files == threads_num:
                st.success("Done! Please click Start to begin the demo")
                break
            time.sleep(1)

if start_button:
    st.snow()

    df, max_time = handle()
    text = []

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

    f"#### Here is the demonstration of :blue[{implementation}]:"
    
    # create an animation object
    ani = FuncAnimation(fig, update_plot, frames=range(max_time+4), interval=1500, repeat=True)
    components.html(ani.to_jshtml(), height=700)

    f"#### Here is the :blue[log] of all threads/processes:"
    for thread_log in text:
        thread_log

    # empty the text for next demo
    text = []
    
    
