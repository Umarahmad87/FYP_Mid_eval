from client import *
import signal
import sys
import threading

Obj = 0
Client = 0

def signal_handler(signal,frame):
    closeAll()
    print 'all closed;;;;'
    time.sleep(1)
    os._exit(1)


signal.signal(signal.SIGINT,signal_handler)



def main():
    Client=client()
    Client.program_start()
if __name__=="__main__":
    main()