from utils import load_times
from csv import writer
import os
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
    with open(csv_file_name, 'w') as f_object:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
        writer_object.writerow(head)
        for i in range(len(files)):
            writer_object.writerow(thread_times[i])
    f_object.close()
    string = algo_name + "was_called."     
    return string