import io
import os
import socket
import struct
import time
import picamera
import picamera.array
import cv2
import numpy as np
import signal
import sys
import threading
import time
import copy as cp
from Queue import Queue
from robot import *
import random
from obstacle_avoid import *

ip = "localhost"
port = 0
camera = 0
connection=0
client_socket=0
no_connection = False
tstop = Queue(maxsize=10)
t_stream = Queue(maxsize=10)
angle_stream = Queue(maxsize=10)
#R = 0


def read_ip():
    global ip,port
    f = open("server_ip.txt", "r")
    ip0 = f.read()
    si = ip0.split(':')
    ip = str(si[0])
    port = int(si[1])
    print 'ip:',ip,'port:',port


def closeAll():
    global camera
    global R
    global D
    global connection
    global client_socket
    camera.stop_preview()
    camera.close()
    R.reset()
    D.reset()
    #tstop.put(False)
    if connection!=0 and client_socket!=0:
        connection.close()
        client_socket.close()
    return



class client:
    def program_start(self):
        Obj = obstacleAvoidence()
        global camera
        global connection
        global client_socket
        global no_connection
        global tstop
        global t_stream
        global angle_stream
        global R
        read_ip()
        #R = RoboCar()
        try:
            
            client_socket = socket.socket()
            client_socket.connect((ip, port))
        # Make a file-like object out of the connection
            connection = client_socket.makefile('wb')
        except:
            no_connection = True

        # Make a file-like object out of the connection
        try:
            camera = picamera.PiCamera()
            camera.resolution = (320, 240)
            # Start a preview and let the camera warm up for 2 seconds
            camera.start_preview(fullscreen=False,window=(100,20,320,240))
            time.sleep(1)

            start = time.time()
            stream = io.BytesIO()
            #make_move_map()
            threading.Thread(target=Obj.make_move).start()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True,quality=10):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                #print 'main'
                #data1 = np.fromstring(stream.getvalue(), dtype=np.uint8)
                #image1 = cv2.imdecode(data1, 1)
                #try:
                #    t_stream.put(dist,False)
                #except:
                #    pass
                if no_connection==False:
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                try:
                    tstop.put(True,False)
                except:
                    pass
            # Rewind the stream and send the image data over the wire
                if no_connection==False:
                    stream.seek(0)
                    connection.write(stream.read())
                else:
                    stream.seek(0)
                    stream.read()
           
                stream.seek(0)
                stream.truncate()
                
        # Write a length of zero to the stream to signal we're done
            if no_connection==False:
                connection.write(struct.pack('<L', 0))
        finally:
            closeAll()
            R.reset()
