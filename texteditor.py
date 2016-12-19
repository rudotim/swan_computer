
import pygame, sys
from pygame.locals import *

from pygame import font

import threading
import types

class texteditor:
    
    maxRows = 6
    currRow = -1
    
    promptStr = ">:"
    cmdstr = ""
    
    maxlen = 50
    textboxes = []
    currbox = -1
    
    boxheight = 0
    cursorRect = Rect(0, 0, 23, 8)
    
    blinkCursor = False
    
    def __init__(self, font, surface):
        self.listeners = {}
        
        self.font = font
        self.surface = surface
        self.boxheight = 40
        
        self.advanceRows()
        
        self.startCursor()
        
        
  
    def golost(self):
        # show box
        box = self.font.render( "Enter the numbers!", 1, (255, 255, 255))
        pos = box.get_rect()        
        pos.y = self.surface.get_rect().centery - (box.get_rect().height/2)
        pos.x = self.surface.get_rect().centerx - (box.get_rect().width/2) 

        rectIn = pos.copy()
        rectIn.inflate_ip( 40, 20 )
        rectOut = rectIn.copy()
        rectOut.inflate_ip( 10, 5 )
        
        rectIn.y += self.boxheight + 30
        rectOut.y += self.boxheight + 30
                
        pygame.draw.rect( self.surface, (255, 0, 0), rectOut, 2)
        pygame.draw.rect( self.surface, (255, 0, 0), rectIn, 1)
        self.surface.blit( box, pos )
        
        
        
        
        
    def processNewChar(self, ascii_num): 
        #print "ascii: " + str(ascii_num)
        #print "char: " + str(chr(ascii_num))
        if ascii_num >= 255:
            return
        
        if self.isAsciiChar(ascii_num):
            self.appendCmdLine( chr(ascii_num) )
        else:
            self.processControlChar(ascii_num)
        
    def processControlChar(self, ascii_num):
        if ascii_num == 13:   # enter
            self.dispatch(msg=self.cmdstr)            
            self.cmdstr = ""
            self.advanceRows()
            
        elif ascii_num == 8:  # backspace
            # backspace
            self.backspaceCmdLine()
        else:
            # ?
            print "Don't know key " + str(ascii_num)
        
        
        
        
    def addNewCmdLineBox(self, promptStr, row):
        
        # create prompt box
        promptTuple = self.createFontBox( promptStr, row )
        
        # create command line box
        cmdTuple = self.createFontBox( "", row )
        
        # create and draw cursor box
        # create rect and include in textbox tuple list
        self.moveCursor( promptTuple[1].width + cmdTuple[1].width, row )
        
        self.textboxes.append( [ promptTuple, cmdTuple ] )        
        
        
        
        
    def backspaceCmdLine(self):
        self.cmdstr = self.cmdstr[:-1]
        self.redrawCmdLine()
        
    def appendCmdLine(self, newch):
        self.cmdstr += newch
        self.redrawCmdLine()
        
        
        
        
        
        
    def startCursor(self):
        print "Starting cursor"
        
        self.blinkCursor = True
        self.makeCursorBlink()
        
    def stopCursor(self):
        print "Stopping cursor"
        self.blinkCursor = False
        self.makeCursorBlink()
        
    def moveCursor(self, x, row):
        print "Erasing last cursor box"
        self.eraseBox( self.cursorRect )
        print "Moving cursor to: " + str(x)
        self.cursorRect.x = x;
        self.cursorRect.y = (row * self.boxheight) + self.boxheight - self.cursorRect.height - 8
        
    def makeCursorBlink(self):
        print "blink!"
        if self.blinkCursor == True:
            # draw cursor at current position
            pygame.draw.rect( self.surface, (51, 225, 51), self.cursorRect)
        else:
            print "Stopping the blink"
            # erase cursor at last position
            self.eraseBox( self.cursorRect )
            
        self.blinkCursor = not self.blinkCursor
        t = threading.Timer(0.4, self.makeCursorBlink)
        t.daemon = True
        t.start()
        
        
        
        
        
        
        
        
    def redrawCmdLine(self):
        
        # erase previous tuples
        box = self.textboxes[self.currbox]
        for tuples in box:
            self.eraseBox( tuples[1] )
         
        # create a new command line text box to the right of the prompt box
        cmdTuple = self.createFontBox( self.cmdstr, self.currRow )
        cmdTuple[1].x = self.textboxes[self.currbox][0][1].right
        
        # update command line tuple         
        self.textboxes[self.currbox][1] = cmdTuple
        
        promptTuple = self.textboxes[self.currbox][0]
        
        # draw cursor relative to current text box  
        self.moveCursor( promptTuple[1].width + cmdTuple[1].width, self.currRow )

        
    def drawCursor(self, cmdLineBox ):
        # erase previous
        #print "prev rect: (" + str(self.cursorRect.x) + ", " + str(self.cursorRect.y) + ") w/h(" + str(self.cursorRect.width) + ", " + str(self.cursorRect.height) + ")"
        self.eraseBox( self.cursorRect )
        rect = Rect(cmdLineBox.right, cmdLineBox.bottom-5, 25, 5)
        pygame.draw.rect( self.surface, (51, 225, 51), rect)
        self.cursorRect = rect 
        #print "new rect: (" + str(self.cursorRect.x) + ", " + str(self.cursorRect.y) + ") w/h(" + str(self.cursorRect.width) + ", " + str(self.cursorRect.height) + ")"
        
        
        
    def advanceRows(self):
                
        self.currbox += 1
        
        boxes = self.getTextAreas()
        
        if self.currRow >= (self.maxRows-1):
            for box in boxes:
                for tuples in box:
                    self.eraseBox( tuples[1] )
                
                    # shift up by one row
                    tuples[1].y -= self.boxheight
        else:
            self.currRow += 1
            
        # add newest command line
        self.addNewCmdLineBox( self.promptStr, self.currRow )
        

        
        
        # ------------------------------
        # Utility Functions
        # ------------------------------
        
    def createFontBox(self, text, row):
        box = self.font.render( text, 1, (51, 204, 51))
        pos = box.get_rect()
        pos.y = (row * self.boxheight)
        return (box, pos)
        
    def eraseBox(self, rect):
        #print "erasin " + str(rect.x) + ", " + str(rect.y) + " to " + str(rect.x + rect.w) + ", " + str(rect.y + rect.h)
        self.surface.fill((0, 0, 0), rect )
        
    def isAsciiChar(self, ascii_num):
        if ascii_num >= 32 and ascii_num <= 126:
            return True
        return False
    
    def isTooLong(self, cmdstr ):
        if len(cmdstr) >= self.maxlen:
            return True
        return False
        
    def getTextAreas(self):            
        return self.textboxes
        
        
        # ----------------------------------
        # Event Handling
        # ----------------------------------
        
    def register(self,listener,events=None):
        """
        register a listener function
         
        Parameters
        -----------
        listener : external listener function
        events  : tuple or list of relevant events (default=None)
        """
        if events is not None and type(events) not in (types.TupleType,types.ListType):
            events = (events,)
              
        self.listeners[listener] = events
         
         
         
    def dispatch(self,event=None, msg=None):
        """notify listeners """
        for listener,events in self.listeners.items():
            if events is None or event is None or event in events:

                try:
                    listener(self,event,msg)
                    #listener(event, msg)
                except Exception as inst:
                    print inst
                    self.unregister(listener)
                    errmsg = "Exception in message dispatch: Handler '{0}' unregistered for event '{1}'  ".format(listener.func_name,event)
                    print errmsg
                    #self.logger.exception(errmsg)
             
    def unregister(self,listener):
        """ unregister listener function """
        del self.listeners[listener]             

        
    