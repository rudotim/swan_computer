#!/usr/bin/python

import os

import pygame
from pygame.locals import *

from lostengine import lostengine
    
    
    
def main():
      
    #editor.register( lost.rcvCommand )
    #cmdstr = ""
    #cmdstrobj = font.render( cmdstr, 1, (51, 204, 51))
    #cmdstrpos = cmdstrobj.get_rect()
    #cmdstrpos.y = background.get_rect().bottom
    #background.blit(cmdstrobj, cmdstrpos)
    
    usingPi = False
    
    lost = lostengine()
    
    lost.init( usingPi )
    lost.mainLoop()

if __name__ == '__main__': main()