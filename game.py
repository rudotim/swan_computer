#!/usr/bin/python

import os
import sys, getopt

import pygame
#from gamecontroller import gamecontroller
import gamecontroller
from pygame.locals import *

from threading import Thread
from time import sleep

from webserver import webserver
from lostengine import lostengine
    
    
    
def main( argv ):
    
    port = 7777
    
    usingPi = False
    cmdString = 'game.py [-p <port>]'
    try:
        opts, args = getopt.getopt(argv,"h",["pi"])
    except getopt.GetoptError:
        print 'error: {0}'.format(cmdString)
        sys.exit(2)
    for opt, arg in opts:
        print opt
        if opt == '-h':
            print 'game.py [-p <port>]'
            sys.exit()
        elif opt in ("-p"):
            port = opt
        elif opt in ("--pi"):
            usingPi = True
    
    try:
        controller = gamecontroller.gamecontroller( usingPi )
        
        # start web server in separate thread
        server = webserver(port, controller)
        thread = Thread(target = server.start, args = [])
        thread.start()
        
        # start lost engine
        lost = lostengine(controller)
        lost.init( usingPi )
        lost.mainLoop()
    except Exception:
        print '^C received, shutting down the web server'
        
    server.stop()
    thread.join()

if __name__ == "__main__":
    main(sys.argv[1:])