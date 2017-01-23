
from videoplayer import videoplayer

class gamecontroller:
    
    def __init__(self, usingPi):
        self.usingPi = usingPi
    
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
