#!/usr/bin/python

import os

import pygame
from pygame.locals import *

from lostengine import lostengine
    
    
    
def main():
      
    usingPi = False
    
    lost = lostengine()
    
    lost.init( usingPi )
    lost.mainLoop()

if __name__ == '__main__': main()