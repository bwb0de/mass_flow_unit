import time
import random
import os 

import pandas as pd
import matplotlib.pyplot as plt

s0_p = [0.0] * 100 # _p primario, _s secundário
s0_s = [0.0] * 100
s1_p = [0.0] * 100
s1_s = [0.0] * 100
s2_p = [0.0] * 100
s2_s = [0.0] * 100
s3_p = [0.0] * 100
s3_s = [0.0] * 100
s4_p = [0.0] * 100
s4_s = [0.0] * 100
s5_p = [0.0] * 100
s5_s = [0.0] * 100
s6_p = [0.0] * 100
s6_s = [0.0] * 100
s7_p = [0.0] * 100
s7_s = [0.0] * 100

range_100 = tuple(range(100))

while True:

    s0_p.append(random.randint(5, 8) / 10)
    s0_s.append(random.randint(3, 6) / 10)
    s1_p.append(random.randint(5, 8) / 10)
    s1_s.append(random.randint(3, 6) / 10)
    s2_p.append(random.randint(5, 8) / 10)
    s2_s.append(random.randint(3, 6) / 10)
    s3_p.append(random.randint(5, 8) / 10)
    s3_s.append(random.randint(3, 6) / 10)
    s4_p.append(random.randint(5, 8) / 10)
    s4_s.append(random.randint(3, 6) / 10)
    s5_p.append(random.randint(5, 8) / 10)
    s5_s.append(random.randint(3, 6) / 10)
    s6_p.append(random.randint(5, 8) / 10)
    s6_s.append(random.randint(3, 6) / 10)
    s7_p.append(random.randint(5, 8) / 10)
    s7_s.append(random.randint(3, 6) / 10)

    for sidx, dados in enumerate([
            (s0_p, s0_s),
            (s1_p, s1_s),
            (s2_p, s2_s),
            (s3_p, s3_s),
            (s4_p, s4_s),
            (s5_p, s5_s),
            (s6_p, s6_s),
            (s7_p, s7_s),
        ]):

        sp, ss = dados

        i = 0
        while len(sp[i:]) > 100:
            i += 1
        
        sp = sp[i:]
        ss = ss[i:]

        fig, ax = plt.subplots()

        ax.plot(range_100, sp, label='Primary', color='blue')
        ax.plot(range_100, ss, label='Secondary', color='red')
        
        ax.fill_between(range_100, sp, color='blue', alpha=0.2)
        ax.fill_between(range_100, ss, color='red', alpha=0.2)
        
        ax.set_title(f'S{sidx}', fontsize=20)
        
        fig.savefig(f'C:\\Users\\Daniel Cruz\\Documents\\Devel\\python\\mass_flow_unit\\static\\img\\S{sidx}.png')
        plt.close()

    time.sleep(1)