import time
import random
import os 

import pandas as pd
import matplotlib.pyplot as plt

s0 = []
s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []
s7 = []

while True:
    s0.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s1.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s2.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s3.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s4.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s5.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s6.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))
    s7.append((random.randint(5, 8) / 10, random.randint(3, 6) / 10))

    images = []
    for i, s in enumerate([s0, s1, s2, s3, s4, s5, s6, s7]):
        df = pd.DataFrame(s, columns=['Prim', 'Sec'])
        df.plot(x='Prim', y='Sec', kind='line')
        
        plt.savefig(f'C:\\Users\\Daniel Cruz\\Documents\\Devel\\python\\mass_flow_unit\\static\\img\\S{i}.png')
        plt.close()

        images.append(f'/static/img/S{i}.png')
    time.sleep(1)