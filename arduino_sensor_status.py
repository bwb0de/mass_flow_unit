import time
import random

from ipvh_srv import set_value

if __name__ == "__main__":
    for n in range(0,10000000):
        set_value('uv', random.randint(0,200))
        time.sleep(2)
