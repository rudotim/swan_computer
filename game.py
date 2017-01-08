#!/usr/bin/python

import os

import pygame
from pygame.locals import *

from threading import Thread
from time import sleep

from webserver import webserver
from lostengine import lostengine
    
    
    
def main():
      
    usingPi = False
    
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

if __name__ == '__main__': main()