#!/usr/local/bin/python3

import os
import sys, getopt

import pygame
#from gamecontroller import gamecontroller
import gamecontroller
from pygame.locals import *

from threading import Thread
from time import sleep

from web.webserver import webserver
from sockysock.socket_comms import socket_comms

from lostengine import lostengine

import signal
    
#global sock_comms
#global threadSock
#global lost
sock_comms = None
threadSock = None
lost = None


    
def main( argv ):
    
    global sock_comms
    global threadSock
    global lost
    
    port = 7777
    
    usingPi = False
    cmdString = 'game.py [-p <port>]'
    try:
        opts, args = getopt.getopt(argv,"h",["pi"])
    except getopt.GetoptError:
        print ('error: {0}'.format(cmdString))
        sys.exit(2)
    for opt, arg in opts:
        print (opt)
        if opt == '-h':
            print ('game.py [-p <port>]')
            sys.exit()
        elif opt in ("-p"):
            port = opt
        elif opt in ("--pi"):
            usingPi = True
    
    signal.signal(signal.SIGINT, signal_handler)

    controller = gamecontroller.gamecontroller(usingPi)

    sock_comms = socket_comms('/tmp/uds_socket', controller);
    threadSock = Thread(target=sock_comms.start, args=[])
    threadSock.start()

    lost = lostengine(controller, quitApp );
    lost.init( usingPi )


    #threadUI = Thread(target=lost.init, args=[ usingPi ])
    #threadUI.start()

#     try:
#         controller = gamecontroller.gamecontroller( usingPi )
#         
#         # start web server in separate thread
#         #server = webserver(port, controller)
#         #thread = Thread(target = server.start, args = [])
#         #thread.start()
#         
#         sock_comms = socket_comms( '/tmp/uds_socket' );
#         threadSock = Thread(target = sock_comms.start, args = [])
#         threadSock.start()
# 
#         lost = lostengine( controller );
#         threadUI = Thread(target = lost.init, args = [ usingPi ])
#         threadUI.start()
#         
#         # start lost engine
#         #lost = lostengine(controller)
#         #lost.init( usingPi )
#         #lost.mainLoop()
#         
#     except Exception:
#         print ('^C received, shutting down the web server')
#         #sock_comms.stop()
#         #threadSock.join()
#    threadSock.join()
    #threadUI.join()
#         server.stop()
#         thread.join()

def signal_handler(sig, frame):
    print("CTRL-C")
    
    lost.stop()
    
    quitApp()

def quitApp():
    print("quitting")
    sock_comms.stop()
    threadSock.join()
        
    #threadUI.join()
    #server.stop()
    #thread.join()

if __name__ == "__main__":
    main(sys.argv[1:])
