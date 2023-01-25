from threading import * 
import time
from random import randint, shuffle
n = int(input("Enter the number of threads: "))
counter = 0
arrival = Semaphore(1)
departure = Semaphore(0)

def barrier(thread_name):
    time.sleep(randint(1,5))
    global counter
    print(thread_name + " has reached the barrier.")
    arrival.acquire()
    counter += 1
    if counter < n:
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
threads = []
for i in range(n):
    thread_name = "Thread " + str(i+1)
    thread = Thread(target= barrier, args = (thread_name,))
    threads.append(thread)
    
shuffle(threads)

for thread in threads:
    thread.start()
