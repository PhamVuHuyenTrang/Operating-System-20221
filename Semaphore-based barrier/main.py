from threading import *         
from Semaphore import Semaphore
from Thread import Thread

counter = 0
arrival = Semaphore(1)
departure = Semaphore(0)

def barrier(thread_name):
    for i in range(6):
        arrival.wait()
        
        print(thread_name + "is running to the barrier.")
        counter += 1
        if counter < n:
            arrival.signal()
            print(thread_name + "has reached the barrier.")
        else:
            departure.signal()
            print("All thread have reached the barrier")
            
        departure.wait()
        print("Unlock threads")
        counter -= 1
        remaining_thread = 6 - counter
        if counter > 0:
            departure.signal()
            print("There are " + str(remaining_thread) + "remaining threads")
        else:
            arrival.signal()
            print("All thread has been unlocked")
        
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
