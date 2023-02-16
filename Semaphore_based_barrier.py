from threading import * 
import time
from random import randint, shuffle
from datetime import datetime
from csv import writer
import pickle
from utils import save_times     

# n = int(input("Enter the number of threads: "))
num = 5
counter = 0
arrival = Semaphore(1)
departure = Semaphore(0)
time_list = []
folder_name = ("./semaphore")

def barrier(thread_name):
    time_list = []
    time_list.append(thread_name)
    global counter
    arrival.acquire()
    start_time = datetime.now()
    time_list.append(start_time)
    time.sleep(randint(1,num))
    counter += 1
    end_time = datetime.now()
    time_list.append(end_time)
    outfile_name = folder_name + "/" + thread_name + ".pkl"
    save_times(time_list, outfile_name)
    print(thread_name + " has reached the barrier.")
    if counter < num:
        arrival.release()
    else:
        departure.release()
        print("-----------------------------------------------")
        print("All threads have reached the barriers. Start unlocking threads.")
    departure.acquire()
    print(thread_name + " has been unlocked") 
    counter -= 1
    if counter > 0:
        departure.release()
    else:
        arrival.release()
        print("All threads have been unlocked")
        
# creating multiple thread 
def main_semaphore(n):  
    global num 
    num = n
    threads = []
    for i in range(n):
        thread_name = "Thread " + str(i+1)
        thread = Thread(target= barrier, args = (thread_name,))
        threads.append(thread)
        
    shuffle(threads)

    for thread in threads:
        thread.start()

