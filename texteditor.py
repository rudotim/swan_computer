
import pygame, sys
from pygame.locals import *

from pygame import font

import threading
import types

from inputbox import inputbox

class texteditor:
    
    maxRows = 6
    currRow = -1
    
    promptStr = ">:"
    
    maxlen = 50
    textboxes = []
    
    boxheight = 0
    cursorRect = Rect(0, 0, 23, 8)
    
    blinkCursor = False
    
    inputbox = None 
    
    def __init__(self, font, surface):
        self.listeners = {}
        
        self.font = font
        self.surface = surface
        self.boxheight = 40
        
        self.advanceRows( self.promptStr, "" )
        self.moveCursor(self.inputbox)
        
        self.startCursor()
        
        
  
    def golost(self):
        # show box
        box = self.font.render( "Enter the numbers!", 1, (255, 255, 255))
        pos = box.get_rect() 
        '''       
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
        
        tmpX = 0
        tmpY = (8 * self.boxheight)
        inpbox = inputbox( "", "4 8 15 16 23 42", tmpX, tmpY, self.font, self.surface )
        inpbox.draw()
        self.moveCursor(inpbox)
        
        self.surface.blit( box, pos )
        '''
        
        
        
        
        
    def processNewChar(self, ascii_num): 
        #print "ascii: " + str(ascii_num)
        #print "char: " + str(chr(ascii_num))
        if ascii_num >= 255:
            return
        
        if self.isAsciiChar(ascii_num):
            self.inputbox.append( chr(ascii_num) )
        else:
            self.processControlChar(ascii_num)
        
        self.moveCursor(self.inputbox)
        
    def processControlChar(self, ascii_num):
        if ascii_num == 13:   # enter
            self.dispatch(msg=self.inputbox.text)            
            self.advanceRows( self.promptStr, "" )
            
        elif ascii_num == 8:  # backspace
            # backspace
            self.inputbox.backspace()
        else:
            # ?
            print "Don't know key " + str(ascii_num)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    def startCursor(self):
        print "Starting cursor"
        
        self.blinkCursor = True
        self.makeCursorBlink()
        
    def stopCursor(self):
        print "Stopping cursor"
        self.blinkCursor = False
        self.makeCursorBlink()
        
    def moveCursor(self, inputbox):
        print "moving cursor to inputbox"
        self.eraseBox( self.cursorRect )
        self.cursorRect.x = inputbox.cursorX # inputbox.getX() + inputbox.getWidth()
        print "rect.width: " + str(inputbox.getWidth())
        self.cursorRect.y = inputbox.cursorY # (inputbox.row * self.boxheight) + self.boxheight - self.cursorRect.height - 8
        
    #def moveCursor(self, x, row):
     #   print "Erasing last cursor box"
      #  self.eraseBox( self.cursorRect )
       # print "Moving cursor to: " + str(x)
        #self.cursorRect.x = x;
        #self.cursorRect.y = (row * self.boxheight) + self.boxheight - self.cursorRect.height - 8
        
    def makeCursorBlink(self):
        #print "blink!"
        if self.blinkCursor == True:
            # draw cursor at current position
            pygame.draw.rect( self.surface, (51, 225, 51), self.cursorRect)
        else:
            #print "Stopping the blink"
            # erase cursor at last position
            self.eraseBox( self.cursorRect )
            
        self.blinkCursor = not self.blinkCursor
        t = threading.Timer(0.4, self.makeCursorBlink)
        t.daemon = True
        t.start()
        
        
        
        
        
        
        
        
        
        
    def injectText(self, text):
        print "inject text!"
        self.advanceRows("", text, False)
        
        
        
    def advanceRows(self, prompt, text, showCursor = True ):
        
        boxes = self.getTextAreas()
        
        if self.currRow >= (self.maxRows-1):
            for box in boxes:
                box.erase()
                
                # shift up by one row
                box.shiftUp()
                    
            # toss first box
            self.textboxes.pop(0)
        else:
            self.currRow += 1
            
        # add newest input box
        self.inputbox = inputbox( prompt, text, 0, self.currRow * self.boxheight, self.font, self.surface )
        self.textboxes.append( self.inputbox )
        
        #if showCursor == True:
        #    self.moveCursor( self.inputbox.getWidth(), self.currRow )
        
        
        
        # ------------------------------
        # Utility Functions
        # ------------------------------
        
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

        
    