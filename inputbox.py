
import pygame, sys
from pygame.locals import *

from pygame import font

class inputbox:
    
    rowTuples = []
    boxheight = 40
    
    def __init__(self, prompt, text, row, font, surface):
        self.font = font
        self.surface = surface
        self.prompt = prompt
        self.text = text
        self.row = row
        
        # create prompt box
        self.promptTuple = self.createFontBox( prompt, row )
        
        # create command line box
        self.textTuple = self.createFontBox( text, row )
        
        self.rowTuples = [ self.promptTuple, self.textTuple ]
        
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
        
    def redraw(self, row ):
        
        # erase previous tuples
        self.erase()
         
        # create a new command line text box to the right of the prompt box
        self.textTuple = self.createFontBox( self.text, row )
        self.textTuple[1].x = self.promptTuple[1].right
        
        # update command line tuple         
        self.rowTuples[1] = self.textTuple;
        
        
    def erase(self):
        for t in self.rowTuples:
            self.surface.fill((0, 0, 0), t[1] )
        
    def createFontBox(self, text, row):
        box = self.font.render( text, 1, (51, 204, 51))
        pos = box.get_rect()
        pos.y = (row * self.boxheight)
        return (box, pos)
        
    def backspace(self):
        self.text = self.text[:-1]
        self.redraw( self.row )
        
    def append(self, newch):
        self.text += newch
        self.redraw( self.row )
        
