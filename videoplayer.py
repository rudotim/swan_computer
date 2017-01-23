
#from omxplayer import OMXPlayer
from time import sleep
from playsound import playsound

class videoplayer:
    
    
    def playAudio(self, audioFilePath):
        playsound( audioFilePath )
        
    def playVideo(self, videoFilePath):
        print "playing video " + videoFilePath
        
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