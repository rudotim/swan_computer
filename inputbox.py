
import pygame, sys
from pygame.locals import *

from pygame import font

class inputbox:
    
    ##  You are converting the constructor to accept x/y pos rather than row
    ##  for positioning.
    
    rowTuples = []
    boxheight = 40
    #cursorX = 0
    #cursorY = 0
    
    #def __init__(self, prompt, text, row, font, surface):
    def __init__(self, prompt, text, x, y, font, surface):
        self.font = font
        self.surface = surface
        self.prompt = prompt
        self.text = text
        self.x = x
        self.y = y 
        #self.row = row
        
        # create prompt box
        self.promptTuple = self.createFontBox( prompt, x, y )
        
        # create command line box
        self.textTuple = self.createFontBox( text, x, y )
        
        self.rowTuples = [ self.promptTuple, self.textTuple ]
        
        # set cursor pos
        self.cursorX = self.getX() + self.getWidth()
        cursorHeight = 8
        self.cursorY = y + self.boxheight - cursorHeight
        
        
    def getCursorPos(self):
        print "get it"
        
    def shiftUp(self):
        for t in self.rowTuples:
            t[1].y -= 40
        
        
    def draw(self):
        for t in self.rowTuples:
            self.surface.blit( t[0], t[1] )
        
    def getX(self):
        return self.promptTuple[1].x

    def getWidth(self):
        return self.promptTuple[1].width + self.textTuple[1].width
        
    def redraw(self, x, y ):
        
        # erase previous tuples
        self.erase()
         
        # create a new command line text box to the right of the prompt box
        self.textTuple = self.createFontBox( self.text, x, y )
        self.textTuple[1].x = self.promptTuple[1].right
        
        # update command line tuple         
        self.rowTuples[1] = self.textTuple;
        
        # set cursor pos
        self.cursorX = self.getX() + self.getWidth()
        cursorHeight = 8
        self.cursorY = self.y + self.boxheight - cursorHeight

        
    def erase(self):
        for t in self.rowTuples:
            self.surface.fill((0, 0, 0), t[1] )
        
    def createFontBox(self, text, x, y):
        box = self.font.render( text, 1, (51, 204, 51))
        pos = box.get_rect()
        #pos.y = (row * self.boxheight)
        pos.x = x
        pos.y = y 
        return (box, pos)
        
    def backspace(self):
        self.text = self.text[:-1]
        self.redraw( self.x, self.y )
        
    def append(self, newch):
        self.text += newch
        self.redraw( self.x, self.y )
        
