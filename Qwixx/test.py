import math
import sys
import time

import numpy as np

d = dict()

for i in range(1,sys.maxsize):
   key = str(i)
   d[key] = key
   if math.log2(i) % 1 == 0: 
     time_start = time.perf_counter()
     value = d[key]
     time_taken = time.perf_counter() - time_start
     print(time_taken*1000*1000, i)