from threading import Thread
from random import shuffle, randint
import time
counter = 0
go = 1
n = int(input("Enter the number of threads: "))
        
def fetch_and_increment():
    global counter
    org = counter
    counter += 1
    return org
  
def barrier(thread_name):
    print(thread_name, "starts now.")
    global counter
    global go
    global n
    
    #thread execution      
    time.sleep(randint(1,5))
    
    #meeting the barrier
    lgo = go
    lcounter = fetch_and_increment()
    print(thread_name, "reached the barrier.\n\tCounter: {}\n\tLocal counter: {}\n\n\tGo: {}\n\tLocal go: {}\n".format(counter, lcounter, go, lgo))
    
    if lcounter + 1 == n:
        counter = 0
        go = 1 - go 
        print(thread_name, "broke the barrier!\nUnlock all threads\n\tCounter: {}\n\tGo: {}\n".format(counter, go)) 
    else:
        while go == lgo:
            time.sleep(5) #await
        print(thread_name, "has been unlocked!") 
               
# creating multiple thread   
threads = []
for i in range(n):
    thread_name = "Thread " + str(i+1)
    thread = Thread(target= barrier, args = (thread_name,))
    threads.append(thread)
    
shuffle(threads)

for thread in threads:
    thread.start()
