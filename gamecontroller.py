
from videoplayer import videoplayer

class gamecontroller:
    
    def __init__(self):
        print "yup, init"
    
    def playVideo(self, video_file):
        videoPath = "res/video/" + video_file
        print "playing video: " + videoPath
        
        vplayer = videoplayer()
        vplayer.playVideo( videoPath )
        
    def playAudio(self, audio_file):
        path = "res/audio/" + audio_file
        print "playing audio: " + path
        
        vplayer = videoplayer()
        vplayer.playAudio( path )    