from robot import *
import threading
from Queue import Queue
import os
import random
R = 0
D = 0
class obstacleAvoidence:

    def make_move(self):
                
        try:
            global R
            global D
            R = RoboMovement()
            D = DistanceCalculation()
            R.setup()
            count = 5
            dist = 0
            choice = [R.left,R.right,R.left,R.right,R.left,R.right,R.left,R.right]
            while True:
                try:
                    dist = D.sonic_distance()
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
                except Exception as e:
                    print e
                    continue
                
                #time.sleep(0.01)
                
        except:
            print "in main except"
            R.reset()
            D.reset()
        finally:
            R.reset()
            D.reset()
    def check(self):
        global R
        R.setup()
        R.left(step=0.9,speed=45)
            