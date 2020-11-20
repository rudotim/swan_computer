
import os

from time import sleep

import pygame
from pygame.locals import *

from ui.texteditor import TextEditor


class SwanEngine:
           
    running = True
    screen = None
    shutdownCallback = None
    
    def __init__(self, controller, shutdown_callback):
        self.controller = controller
        self.shutdownCallback = shutdown_callback
        self.controller.setTextReceiver(self.inject_text)

        self.background = None
        self.editor = None
        
    def on_pi(self):
        print ("On RPI")
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print ("I'm running under X display = {0}".format(disp_no))
        
        #os.environ["SDL_FBDEV"] = "/dev/fb0"
        #pygame.init()
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['directfb', 'fbcon', 'xvfb', 'x11', 'dga', 'ggi', 'vgl', 'svgalib', 'aalib', 'windib', 'directx'] 
        #the last 2 are windows where we should not need the fb since it always has desktop, but lets keep them anyway...
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                print("Driver: " + driver)
                pygame.display.init()
            except pygame.error:
                print('Driver: {0} failed.'.format(driver))
                continue
            found = True
            break
        
        if not found:
            raise Exception('No suitable video driver found!')
        else:
            # Initialise screen
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
            print ("Framebuffer size: %d x %d" % (size[0], size[1]))
            return pygame.display.set_mode(size, pygame.FULLSCREEN)

    def init(self, pi):

        pygame.init()

        if pi:
            self.screen = self.on_pi()
        else:
            self.screen = pygame.display.set_mode((640, 480)) # , FULLSCREEN) DO NOT USE THIS UNLESS YOU HAVE EXIT

        # Clear the screen to start
        #self.screen.fill((150, 150, 150))
        self.screen.fill((0, 0, 0))

        pygame.font.init()
        
        pygame.display.set_caption('Lost Emulator')
    
        # Fill background
        self.background = pygame.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))
    
        # Load Apple II font
        font = pygame.font.Font("res/fonts/PrintChar21.ttf", 26)
        
        # Blit everything to the screen
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
        #pygame.display.flip()

        dimensions = Rect(0, 0, 640, 480)
        self.editor = TextEditor( dimensions, font, self.background, self.controller)
        self.editor.register(self.receive_command)

        self.main_loop()
        
    def main_loop(self):
        # Event loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.editor.process_new_char( event.key)

            self.screen.blit(self.background, (0, 0))
            pygame.display.update()
            #pygame.display.flip()
            sleep(0.05)
        print("DONE RUNNING")
        
    def stop(self):
        print("stopping UI")
        self.running = False
        self.shutdownCallback()

    def receive_command(self, sender, event, msg=None):
        print("You got event {0} with message {1}".format(event, msg))
        if msg == "lost":
            self.initiate_lost_numbers()
        elif msg == "":
            pass
        elif msg == "txt":
            self.editor.output_text("Hey It's me, Walt!")
        elif msg == "video":
            self.controller.playVideo("swan.mp4")
        elif msg == "audio":
            self.controller.playAudio("Code ok.mp3")
        elif msg == "4 8 15 16 23 42":
            self.controller.lostNumbersEntered()
        elif msg == "count":
            self.controller.resetCountdown(10)
        elif msg == "countstop":
            self.controller.stopCounting()
        elif msg == "exit":
            print("exiting")
            self.stop()
        else:
            self.editor.output_text("Syntax Error")

    def inject_text(self, text):
        print("injecting text> ", text)
        self.editor.inject_text(text)

    def initiate_lost_numbers(self):
        print ("You gots to imput da numbaz!")
        self.editor.golost()