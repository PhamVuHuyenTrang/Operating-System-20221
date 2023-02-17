from threading import Thread
from random import shuffle, randint
import time
from datetime import datetime
from utils import save_times

'''
shared variables
'''
leader = 0  # test-and-set bit
countflag = 0  # test-and-test-and-set bit
go = 1  # atomic bit

folder_name = ("./test_and_set")

def test_and_set_leader():
    global leader
    orig = leader
    leader = 1
    return orig

def test_and_set_countflag():
    global countflag
    orig = countflag
    countflag = 1
    return orig

def barrier(thread_name):
    global go
    global countflag
    global leader
    global n
    local_go = go
    # execute thread
    time.sleep(randint(1, 5))
    time_list = []

    if test_and_set_leader() == 0:  # leader process
        local_count = 0
        start_time = datetime.now() 
        time_list = []
        time_list.append(thread_name)
        time_list.append(start_time)
            
        print(f'Leader - {thread_name} started.')

        while local_count < (n-1):
            # await
            while (countflag != 1):
                time.sleep(2)
            local_count += 1
            print(f'{thread_name} is at the barrier.')
            arrival_time = datetime.now()
            time_list.append(arrival_time)
            outfile_name = folder_name + "/" + thread_name + ".pkl"
            save_times(time_list, outfile_name)
            
            countflag = 0  # reset to 0
        print("=============================================")
        print(f"All processes has arrived. Leader process local counter equal {local_count}. Exiting barrier...")
        
        # exit
        leader = 0  # reset
        go = 1 - go
        print(f'{thread_name} exited barrier.')

    else:  # other processes
        print(f'Thread {thread_name} started.')
        start_time = datetime.now()
        time_list.append(thread_name)
        time_list.append(start_time)

        while (test_and_set_countflag() != 0):
            time.sleep(1)
        print(f'Countflag equals {countflag}, {thread_name} is at the barrier.')
        arrival_time = datetime.now()
        time_list.append(arrival_time)
        outfile_name = folder_name + "/" + thread_name + ".pkl"
        save_times(time_list, outfile_name)

        while (local_go == go):
            time.sleep(2)

        print(f'{thread_name} exited barrier.')

def run_test_and_set(num):
    print("Running Test and set Algorithm...")
    global n
    n = num
    # creating threads
    threads = []
    for i in range(num):
        thread_name = "Thread " + str(i+1)
        thread = Thread(target=barrier, args=(thread_name, ))
        threads.append(thread)

    shuffle(threads)

    for thread in threads:
        thread.start()

# if __name__ == '__main__':
#     try:
#         n = int(input('Enter the number of threads: '))
#         if n <= 1:
#             raise Exception
#     except ValueError as e:
#         raise ValueError('Number of threads should be an integer').with_traceback(e.__traceback__)
#     except Exception as e:
#         raise Exception('Number of threads should be larger than 1')
    
#     run_test_and_set(n)
