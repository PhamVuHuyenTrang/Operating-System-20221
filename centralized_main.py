from threading import Thread
from random import shuffle
counter = 0
go = 1
n = 6  
        
def fetch_and_increment():
    global counter
    org = counter
    counter += 1
    return org

#print(fetch_and_increment())
#print(counter)    
def barrier(thread_name):
    global counter
    global go
    global n
    
    lgo = go
    lcounter = fetch_and_increment()
    
    print(thread_name, "reached the barrier.")
    if lcounter + 1 == n:
        print(thread_name, "broke the barrier! Unlock all threads\n")
        counter = 0
        go = 1 - go      
    else:
        while go == lgo:
            pass
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