
#from omxplayer import OMXPlayer
from time import sleep

from playsound import playsound
import pygame.locals
import pygame.time
#from __builtin__ import False
import subprocess


class videoplayer:
    
    
    def playAudio(self, audioFilePath):
        playsound( audioFilePath )
        
    def playVideo(self, videoFilePath):
        print ("playing video " + videoFilePath)
        myplaylist = "/home/desmond/swan/lost_emulator/res/video/swan.mp4"
        subprocess.call(['mplayer', '-vo', 'sdl', '-ao', 'alsa', myplaylist])
#         FPS = 60
# 
#         clock = pygame.time.Clock()
#         movie = pygame.movie.Movie(videoFilePath)
#         screen = pygame.display.set_mode(movie.get_size())
#         movie_screen = pygame.Surface(movie.get_size()).convert()
#         
#         movie.set_display(movie_screen)
#         movie.play()
#                 
#         playing = True
#         while playing:
#             for event in pygame.event.get():
#                 if event.type == pygame.KEYDOWN:
#                     if event.key == 13:   # enter
#                         print ("enter!")
#                         movie.stop()
#                         playing = False
#                                         
#                 if event.type == pygame.QUIT:
#                     movie.stop()
#                     playing = False
#         
#             screen.blit(movie_screen,(0,0))
#             pygame.display.update()
#             clock.tick(FPS)
        # This will start an `omxplayer` process, this might
        # fail the first time you run it, currently in the
        # process of fixing this though.
        #player = OMXPlayer(videoFilePath)
        
        # The player will initially be paused
        
        #player.play()
        ##sleep(5)
        ##player.pause()
        
        # Kill the `omxplayer` process gracefully.
        #player.quit()