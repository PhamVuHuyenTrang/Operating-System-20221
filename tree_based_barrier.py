import threading
import time
import math
from datetime import datetime
from utils import save_times
from random import randint

folder_name = ("./tree_barrier")
thread_nums = 1
# time_list = []

class Node:
    def __init__(self, size, id = None, parent=None):
        """
        Initialize a node with a size, id, and parent. 
        """
        self.size = size
        self.parent = parent
        self.id = id 
        self.lock_sense = False
        self.count = size
        self.root = False
        self.lock = threading.Lock()
    
    def set_child(self, other):
        """
        Set another node to be the child of this node
        """
        other.parent = self 
        self.size +=1
        self.count += 1

    def fetch_and_decrement(self):
        """
        Atomically decrement the count and return the current value.
        """
        self.lock.acquire()
        current_value = self.count
        self.count -= 1
        self.lock.release()
        return current_value
    
    def __str__(self):
        return self.id

sense = True 

def wait(node):
    """
    Function that each thread calls to wait at the barrier.
    """
    global sense
    print(f"{node.id} reach the barrier")

    if node.parent.fetch_and_decrement() == 1:
        if node.parent is not None and node.parent.root != True:
            wait(node.parent)
        print(f"{node.parent.id} is release from the barrier")
    
        node.parent.count = node.parent.size
        node.parent.lock_sense = not node.parent.lock_sense
 
    while node.parent.lock_sense != sense:
        pass

def buildTree(num_threads):
    """
    Builds a binary tree with num_threads leaves.
    """
    tree = []
    num_nodes = num_threads
    layers = 0
    while num_nodes >= 1:
        layer = []
        for i in range(num_nodes):
            if layers == 0:
                new_node = Node(0, id = "Thread "+ str(i))
            else:               
                new_node = Node(0, id = str(layers)+"-"+str(i))
                new_node.set_child(tree[layers-1][2*i])
                try:
                    new_node.set_child(tree[layers-1][2*i+1])
                except:
                    pass
                if layers == math.ceil(math.log2(num_threads)):
                    new_node.root = True
            layer.append(new_node)
        tree.append(layer)
        
        if num_nodes == 1:
            break
        num_nodes = math.ceil(num_nodes/2)
        layers += 1

    return tree


def worker(node):
    """
    Function run by each thread.
    """
    global thread_nums
    print("Thread {} is starting".format(node.id))
    start_time = datetime.now()
    time_list = []
    time_list.append(node.id)
    time_list.append(start_time)

    # Do some work
    time.sleep(randint(2,thread_nums))

    end_time = datetime.now()
    time_list.append(end_time)
    outfile_name = folder_name + "/" + node.id + ".pkl"
    save_times(time_list, outfile_name)
    wait(node)

    print("Thread {} is done".format(node.id))


def run_tree_barrier(num_threads):
    global thread_nums
    thread_nums = num_threads
    barrier = buildTree(num_threads)

    threads = []
    for i in barrier[0]:
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        time.sleep(randint(1,2))
        t.start()
    
    for t in threads:
        t.join()
    
    print("All threads are done!")
