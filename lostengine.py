
import os

from time import sleep

import pygame
from pygame.locals import *

from texteditor import texteditor

class lostengine:
           
    running = True
    
    def onPi(self):
        print "On RPI"
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        os.environ["SDL_FBDEV"] = "/dev/fb0"
        pygame.init()
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['directfb', 'fbcon', 'directfb', 'svgalib', 'xvfb', 'x11', 'dga', 'ggi', 'vgl', 'svgalib', 'aalib', 'windib', 'directx'] 
        #the last 2 are windows where we should not need the fb since it always has desktop, but lets keep them anyway...
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            #if not os.getenv('SDL_VIDEODRIVER'):
            #        os.putenv('SDL_VIDEODRIVER', driver)
            try:
                    print("Driver: "+driver)
                    #pygame.display.init()
            except pygame.error:
                    print 'Driver: {0} failed.'.format(driver)
                    continue
            found = True
            print("this one works.")
            break
        
        # Initialise screen
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

        if not found:
            raise Exception('No suitable video driver found!')

    def init(self, pi):
        if pi == True:
            self.onPi()
        else:
            self.screen = pygame.display.set_mode((640, 480)) # , FULLSCREEN) DO NOT USE THIS UNLESS YOU HAVE EXIT
           
        #pygame.init()
        #screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((150, 150, 150))        
        
        pygame.font.init()
        #x, y = screen.get_size()
        
        pygame.display.set_caption('Lost Emulator')
    
        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
    
        # Load Apple II font
        font = pygame.font.Font("PrintChar21.ttf", 26)
        
        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
        #pygame.display.flip()
        
        self.editor = texteditor( font, self.background ) 
        self.editor.register( self.rcvCommand )
        
    def mainLoop(self):
        # Event loop
        while self.running == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.editor.processNewChar( event.key )                
            
            # get text boxes from editor
            lines = self.editor.getTextAreas()
            for line in lines:
                line.draw()
                        
            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            #pygame.display.flip()
            sleep(0.05)
        
    def rcvCommand(self,sender,event,msg=None):
        print "You got event {0} with message {1}".format(event,msg)
        if msg == "lost":
            self.initiateLostNumbers()
        elif msg == "txt":
            self.editor.injectText("Hey It's me, Walt!")
        elif msg == "video":
            self.editor.playVideo( "swan.mp4" )
        elif msg == "exit":
            print "exiting"
            self.running = False

    def initiateLostNumbers(self):
        print "You gots to imput da numbaz!"
        self.editor.golost()
        