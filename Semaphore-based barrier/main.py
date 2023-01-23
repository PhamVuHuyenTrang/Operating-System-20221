from threading import *         
import time

n = int(input("Enter the number of threads: "))
count = 0
mutex = Semaphore(1)
barrier = Semaphore(0)


mutex.release()
count = count + 1
mutex.acquire()

if count == n: 
    barrier.acquire() # unblock ONE thread

barrier.release()
barrier.acquire() # once we are unblocked, it's our duty to unblock the next thread