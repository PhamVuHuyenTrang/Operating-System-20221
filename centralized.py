from threading import *
from random import shuffle, randint
import time
from datetime import datetime
from csv import writer
import pickle
from utils import save_times  

counter = 0
go = 1
#n = 6
num = 5
time_list = []
folder_name = ('./centralized')      
def fetch_and_increment():
    global counter
    org = counter
    counter += 1
    return org
  
def barrier(thread_name):
    #print(thread_name, "starts now.")
    start_time = datetime.now()
    time_list = []
    time_list.append(thread_name)
    time_list.append(start_time)
    
    global counter
    global go
    #global n
    
    #thread execution      
    time.sleep(randint(1,num))
    end_time = datetime.now()
    time_list.append(end_time)
    outfile_name = folder_name + "/" + thread_name + ".pkl"
    save_times(time_list, outfile_name)
    #meeting the barrier
    lgo = go
    lcounter = fetch_and_increment()
    #print(thread_name, "reached the barrier.\n\tCounter: {}\n\tLocal counter: {}\n\n\tGo: {}\n\tLocal go: {}\n".format(counter, lcounter, go, lgo))
    
    if lcounter + 1 == num:
        counter = 0
        go = 1 - go 
        #print(thread_name, "broke the barrier!\nUnlock all threads\n\tCounter: {}\n\tGo: {}\n".format(counter, go)) 
    else:
        while go == lgo:
            time.sleep(5) #await
        #print(thread_name, "has been unlocked!") 
               
# creating multiple thread 
def main_centralized(n):
    global num
    num = n  
    threads = []
    for i in range(n):
        thread_name = "Thread " + str(i+1)
        thread = Thread(target= barrier, args = (thread_name,))
        threads.append(thread)
    
    shuffle(threads)

    for thread in threads:
        time.sleep(randint(1,n))
        thread.start()
