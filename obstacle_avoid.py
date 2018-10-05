from robot import *
import threading
from Queue import Queue
import os
import random

R = RoboCar()
t_dist = Queue(maxsize=1)
def closeAll():
    global R
    R.reset()
    return

def signal_handler(signal,frame):
    closeAll()
    print 'all closed;;;;'
    time.sleep(1)
    os._exit(1)

class obstacle_avoid:
    def program_start(self):
        try:
            global R
            R.setup()
            count = 5
            dist = 0
            choice = [R.left,R.right,R.left,R.right,R.left,R.right,R.left,R.right]
            while True:
                try:
                    dist = R.sonic_distance()
                    print "Distance = ",dist
                    if dist>35:
                        R.forward(step=0.5,speed=50)
                        if count<=0:
                            R.right(step=0.15,speed=50)
                            count=6
                        
                    else:
                        ch_index = random.randint(0, 8)
                        print "selected function = ",ch_index
                        choice[ch_index](step=0.9,speed=45)
                        
                    count-=1
                    time.sleep(0.05)
                except:
                    print "in continue"
                    continue
                
                #time.sleep(0.01)
                
        except:
            print "in main except"
            R.reset()
        finally:
            R.reset()
    def check(self):
        global R
        R.setup()
        R.left(step=0.9,speed=45)
            