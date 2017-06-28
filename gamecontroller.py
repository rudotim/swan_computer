
from countdown_thread import countdown_thread
from videoplayer import videoplayer


class gamecontroller:
    
    countdownThread = None
    
    def __init__(self, usingPi):
        self.usingPi = usingPi
        self.countdownThread = countdown_thread(self)
    
    def playVideo(self, video_file):
        videoPath = "res/video/" + video_file
        print "playing video: " + videoPath
        
        if self.usingPi:
            vplayer = videoplayer()
            vplayer.playVideo( videoPath )
        else:
            print "simulating video: " + videoPath
        
    def playAudio(self, audio_file):
        path = "res/audio/" + audio_file
        print "playing audio: " + path
        
        if self.usingPi:
            vplayer = videoplayer()
            vplayer.playAudio( path )    
        else:
            print "simulating audio: " + path
            
    def resetCountdown(self, seconds):
        self.countdownThread.resetCountdown(seconds)
        
    def stopCounting(self):
        self.countdownThread.stopCounting()
        
        
