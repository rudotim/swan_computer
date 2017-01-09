#!/usr/bin/python

import os
import sys, getopt

import pygame
from pygame.locals import *

from threading import Thread
from time import sleep

from webserver import webserver
from lostengine import lostengine
    
    
    
def main( argv ):
    
    usingPi = False
    try:
        opts, args = getopt.getopt(argv,"h",["pi"])
    except getopt.GetoptError:
        print 'error: test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        print opt
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("--pi"):
            usingPi = True
    
    try:
        # start web server in separate thread
        server = webserver(7777)
        thread = Thread(target = server.start, args = [])
        thread.start()
        
        # start lost engine
        lost = lostengine()
        lost.init( usingPi )
        lost.mainLoop()
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        
    server.stop()
    thread.join()

if __name__ == "__main__":
    main(sys.argv[1:])