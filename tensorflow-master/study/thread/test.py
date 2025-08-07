#import numpy as np
#import os
#import sys
import threading

#print(sys.executable)
#print(os.path.dirname(sys.executable))
#print("Hello world")
#print(np.mean([100, 50]))

def sum(name, low, high):
    total = 0
    for i in range(low, high):
        total += i
    print("Subthread", total)

t = threading.Thread(target=sum, args=('test',1000, 100000))
t.start()

print("Main Thread")
