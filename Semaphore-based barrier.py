from threading import * 
import time
from random import randint

counter = 0
arrival = Semaphore(1)
departure = Semaphore(0)

def barrier(thread_name):
    time.sleep(randint(1,5))
    global counter
    print(thread_name + " has reached the barrier.")
    arrival.acquire()
    counter += 1
    if counter < 6:
        arrival.release()
    else:
        departure.release()
        print("-----------------------------------------------")
        print("All threads have reached the barriers")
    departure.acquire()
    print(thread_name + " has been unlocked") 
    counter -= 1
    if counter > 0:
        departure.release()
    else:
        arrival.release()
        print("All threads have been unlocked")
        
# creating multiple thread   
thread_1 = Thread(target = barrier , args = ('Thread 1',))  
thread_2 = Thread(target = barrier, args = ('Thread 2',))  
thread_3 = Thread(target = barrier , args = ('Thread 3',))  
thread_4 = Thread(target = barrier , args = ('Thread 4',))  
thread_5 = Thread(target = barrier , args = ('Thread 5',))  
thread_6 = Thread(target = barrier , args = ('Thread 6',))  
  
# calling the threads   
thread_1.start()  
thread_2.start()  
thread_3.start()  
thread_4.start()  
thread_5.start()  
thread_6.start()  