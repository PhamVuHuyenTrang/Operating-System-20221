from utils import load_times
from csv import writer
import os
import pandas as pd

# algo_name = test_and_set, semaphore, centralized, tree
def run(algo_name):
    thread_times = []
    folder_name = "./" + algo_name
    files = os.listdir(folder_name)
    for i in range(len(files)):
        files[i] = folder_name + "/" + files[i]
    for file in files:
        thread_time = load_times(file)
        thread_times.append(thread_time)
    
    start_times = []
    for i in range(len(thread_times)):
        start_times.append(thread_times[i][1])
    
    start_point = min(start_times)
    for i in range(len(thread_times)):
        thread_times[i][1] = round((thread_times[i][1] - start_point).total_seconds())
        thread_times[i][2] = round((thread_times[i][2] - start_point).total_seconds())
    #Export time to a csv file 
    head = ['thread', 'start_time', 'arrival_time']
    csv_file_name = algo_name + ".csv"  

    thread_dict = {}
    thread_dict['thread'] = [x[0] for x in thread_times]
    thread_dict['start_time'] = [x[1] for x in thread_times]
    thread_dict['arrival_time'] = [x[2] for x in thread_times]

    max_arrival_time = max(thread_dict['arrival_time'])

    df_thread = pd.DataFrame(thread_dict)
    df_thread.to_csv(csv_file_name, index=False)

    return df_thread, max_arrival_time

