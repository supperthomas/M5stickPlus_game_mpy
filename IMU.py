from m5stack import *
from m5ui import *
from uiflow import *
import imu
from time import sleep
asdf = None
i = None
a = None

while True:
    imu0 = imu.IMU()
    c = imu0.acceleration[0]
    z = imu0.acceleration[2]
    print("acceleration[0] x ",c)
    print("acceleration[2] z ",z)
    if c>0 and c > 0.2 :
        if(c > 0.5):
            print("fast left")
        else:
            print("left")
    elif c<0 and c < -0.2:
        if(c < -0.5):
            print("fast right")
        else:
            print("right")
    print("=======")
    time.sleep(1)
    

