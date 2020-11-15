
import pygame, sys
from pygame.locals import *

from pygame import font
#from videoplayer import videoplayer
#import videoplayer

import threading
import types

from ui.text_editor_specs import text_editor_specs
from collections import deque


class TextEditor:

    class PromptData:
        def __init__(self, prompt_font, prompt_str):
            self.prompt_str = prompt_str
            self.prompt_box = prompt_font.render(self.prompt_str, 1, (51, 204, 51))

        def width(self):
            return self.prompt_box.get_width()

    # text data
    text_queue = deque()
    current_text_line = ""

    input_queue = deque()
    output_queue = deque()

    # size of cursor rectangle
    cursorRect = Rect(0, 0, 23, 8)
    
    currRow = -1

    blinkCursor = False

    def __init__(self, dimensions, font, surface, controller):
        self.listeners = {}

        # Rect defining the bounds of this text editor
        self.dimensions = dimensions

        self.controller = controller

        # pygame font object
        self.font = font

        # pygame background surface
        self.surface = surface

        self.font_height = self.get_font_height()
        self.cursor_x = 0

        # text editor options
        self.specs = text_editor_specs()

        self.prompt = self.PromptData(font, ":>")

        self.redraw()
        self.start_cursor()
        
        
    def get_font_height(self):
        """ Determine line height of this font
        """
        box = self.font.render("a", 0, (0, 0, 0))
        return box.get_height()


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
        
        
        
    # ------------------------------
    # Text Processing 
    # ------------------------------

    def process_new_char(self, ascii_num):
        if ascii_num >= 255:
            return
        
        if self.is_ascii_char(ascii_num):

            self.current_text_line += chr( ascii_num )
            self.redraw()
        else:
            self.process_control_char(ascii_num)

        self.redraw()
        #self.update_cursor_pos()


    def process_control_char(self, ascii_num):
        if ascii_num == 13:   # enter
            command_txt = self.current_text_line

            # save to input queue
            self.input_queue.appendleft( command_txt )

            # reset cursor to start of line
            self.cursor_x = 0

            # advance the rows down the screen
            self.advance_rows_with_text()

            self.dispatch(msg=command_txt)

        elif ascii_num == 8:  # backspace
            self.current_text_line = self.current_text_line[0:len(self.current_text_line)-1]
        else:
            # ?
            print("Don't know key " + str(ascii_num))
        

    def start_cursor(self):
        self.blinkCursor = True
        self.make_cursor_blink()


    def stop_cursor(self):
        self.blinkCursor = False
        self.make_cursor_blink()


    def update_cursor_pos(self, x, y):
        self.erase_box( self.cursorRect)
        self.cursorRect = Rect(
            x, y, 23, 8)


    def make_cursor_blink(self):
        if self.blinkCursor:
            # draw cursor at current position
            pygame.draw.rect( self.surface, (51, 225, 51), self.cursorRect)
        else:
            # erase cursor at last position
            self.erase_box( self.cursorRect)

        self.blinkCursor = not self.blinkCursor
        t = threading.Timer(0.4, self.make_cursor_blink)
        t.daemon = True
        t.start()


    def inject_text(self, text):
        self.advance_rows_with_text(text, False)


    def output_text(self, text):
        self.output_queue.appendleft( text )
        self.advance_rows_with_text(text, False)


    def advance_rows_with_text(self, text=None, fromLocalUser = True):

        # add command line to the text history
        if text is None:
            self.text_queue.appendleft( self.prompt.prompt_str + self.current_text_line )
            #self.text_queue.appendleft( self.current_text_line )
            self.current_text_line = ""
        else:
            # output text
            if self.output_queue.__len__() > 0:
                self.text_queue.appendleft( self.output_queue.pop() )


    def draw_prompt(self, row):
        dest_rec = (0, row * self.font_height, self.prompt.width(), self.font_height)
        self.surface.blit(self.prompt.prompt_box, dest_rec)


    def redraw(self):
        row = 0

        self.surface.fill( pygame.Color("black") )
        for t in reversed(self.text_queue):
            row = self.draw_lines( row, t, False )

        self.draw_lines(row, self.current_text_line, True)


    def draw_lines(self, row, text, show_prompt=False):
        new_row = row
        text_len = len(text)

        # keep track of whether or not prompt is present
        # include prompt chars in check for overflow

        prompt_width = self.prompt.width() if show_prompt else 0
        if show_prompt:
            self.draw_prompt(new_row)
            text_len += len(self.prompt.prompt_str)
        if text_len >= self.specs.maxCols:
            # split text
            start = 0
            end = self.specs.maxCols - (0 if not show_prompt else len(self.prompt.prompt_str))
            while start <= text_len:
                txt = text[start:end]
                print("rendering multiline>", txt)
                start = end
                end += self.specs.maxCols

                cmd_text_box = self.font.render( txt, 1, (51, 204, 51))
                dest_rec = (prompt_width if row == new_row else 0,
                    new_row * self.font_height,
                    self.dimensions[2],
                    self.font_height)
                self.cursor_x = prompt_width if row == new_row else 0 + cmd_text_box.get_width()
                self.surface.blit(cmd_text_box, dest_rec)
                self.update_cursor_pos(self.cursor_x, (new_row + 1) * self.font_height)

                new_row += 1
                text_len = len(text)
        else:
            # draw command line text
            cmd_text_box = self.font.render( text, 1, (51, 204, 51))
            dest_rec = (prompt_width , new_row * self.font_height, self.dimensions[2], self.font_height)
            self.surface.blit(cmd_text_box, dest_rec)
            self.cursor_x = self.prompt.width() + cmd_text_box.get_width()
            self.update_cursor_pos( self.cursor_x, (new_row+1) * self.font_height )
            new_row += 1

        return new_row

    # ------------------------------
    # Utility Functions
    # ------------------------------
        
    def erase_box(self, rect):
        #self.surface.fill((255, 0, 0), rect )
        pass

    @staticmethod
    def is_ascii_char(ascii_num):
        if 32 <= ascii_num <= 126:
            return True
        return False


    def is_too_long(self, cmdstr):
        if len(cmdstr) >= self.specs.maxLen:
            return True
        return False
        

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
        if events is not None and type(events) not in (types.TupleType, types.ListType):
            events = (events,)
              
        self.listeners[listener] = events
         
         
         
    def dispatch(self,event=None, msg=None):
        """notify listeners """
        for listener,events in self.listeners.items():
            if events is None or event is None or event in events:

                try:
                    listener(self, event, msg)
                    #listener(event, msg)
                except Exception as inst:
                    print (inst)
                    self.unregister(listener)
                    errmsg = "Exception in message dispatch: Handler '{0}' unregistered for event '{1}'  ".format(listener.func_name, event)
                    print (errmsg)
                    #self.logger.exception(errmsg)
             
    def unregister(self, listener):
        """ unregister listener function """
        del self.listeners[listener]             
