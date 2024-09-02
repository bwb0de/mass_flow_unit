import time

from ipvh_srv import get_value

if __name__ == "__main__":
    for n in range(0,10000000):
        print(get_value('uv'))
        time.sleep(0.01)



    
    







