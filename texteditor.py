
import pygame, sys
from pygame.locals import *

from pygame import font

import types

class texteditor:
    
    cmdstr = ""
    maxlen = 50
    textboxes = []
    currbox = 0
    
    boxheight = 0
    cursorRect = Rect(0, 0, 0, 0)
    
    def __init__(self, font, surface):
        self.listeners = {}
        
        self.font = font
        self.surface = surface
        
        self.addNewCmdLineBox()
                
        self.boxheight = self.textboxes[0][0].get_rect().height
        
        
        
        
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
        #ch = chr(ascii_val)       
        if self.isAsciiChar(ascii_num):
            self.appendCmdLine( chr(ascii_num) )
        else:
            self.processControlChar(ascii_num)
        
    def processControlChar(self, ascii_num):
        if ascii_num == 13:   # enter
            self.dispatch(msg=self.cmdstr)            
            self.advanceAllBoxes()
            self.cmdstr = ""
            self.currbox += 1
            # create new box
            self.addNewCmdLineBox()
            
        elif ascii_num == 8:  # backspace
            # backspace
            self.backspaceCmdLine()
        else:
            # ?
            print "Don't know key " + str(ascii_num)
        
    def advanceAllBoxes(self):
        boxes = self.getTextAreas()
        for box in boxes:
            self.eraseBox( box[1] )
            # shift up by X
            box[1].y -= self.boxheight
            
        self.eraseFullCmdLine()
        
    def addNewCmdLineBox(self):
        tmp = self.font.render( "", 1, (255, 255, 255))
        pos = tmp.get_rect()        
        pos.y = self.surface.get_rect().bottom - 40
        
        self.textboxes.append( (tmp, pos) )
        self.drawCursor( pos )
        pygame.draw.rect( self.surface, (225, 0, 225), pos, 1)
        
    def eraseFullCmdLine(self):
        self.eraseBox( (0, 440, 400, self.boxheight) )
        
    def eraseBox(self, rect):
        #print "erasin " + str(rect.x) + ", " + str(rect.y) + " to " + str(rect.x + rect.w) + ", " + str(rect.y + rect.h)
        self.surface.fill((0, 0, 0), rect )

        
    def isAsciiChar(self, ascii_num):
        if ascii_num >= 32 and ascii_num <= 126:
            return True
        return False
        
    def backspaceCmdLine(self):
        self.cmdstr = self.cmdstr[:-1]
        self.redrawCmdLine()
        
        
    def appendCmdLine(self, newch):
        self.cmdstr += newch
        self.redrawCmdLine()
        
    def redrawCmdLine(self):
        # erase previous box
        self.eraseBox( self.textboxes[self.currbox][1] )
        
        newbox = self.font.render( self.cmdstr, 1, (51, 204, 51))
        newbox.get_rect().y = self.surface.get_rect().bottom - 40
        pos = newbox.get_rect()
        pos.y = self.surface.get_rect().bottom - 40
                 
        self.textboxes[self.currbox] = (newbox, pos)  
        self.drawCursor( pos )          
        pygame.draw.rect( self.surface, (0, 0, 225), pos, 1)
        
    def drawCursor(self, cmdLineBox ):
        # erase previous
        #print "prev rect: (" + str(self.cursorRect.x) + ", " + str(self.cursorRect.y) + ") w/h(" + str(self.cursorRect.width) + ", " + str(self.cursorRect.height) + ")"
        self.eraseBox( self.cursorRect )
        rect = Rect(cmdLineBox.right, cmdLineBox.bottom-5, 25, 5)
        pygame.draw.rect( self.surface, (51, 225, 51), rect)
        self.cursorRect = rect 
        #print "new rect: (" + str(self.cursorRect.x) + ", " + str(self.cursorRect.y) + ") w/h(" + str(self.cursorRect.width) + ", " + str(self.cursorRect.height) + ")"
        
    def isTooLong(self, cmdstr ):
        if len(cmdstr) >= self.maxlen:
            return True
        return False
        
    def getTextAreas(self):            
        return self.textboxes
        
    