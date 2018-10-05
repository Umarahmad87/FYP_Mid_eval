from obstacle_avoid import *
import signal
import sys
import threading

signal.signal(signal.SIGINT,signal_handler)
def main():
    Obj = obstacle_avoid()
    Obj.program_start()
    #Obj.check()

if __name__=="__main__":
    main()