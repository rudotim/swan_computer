
#from omxplayer import OMXPlayer
import threading
from time import sleep

from playsound import playsound
from __builtin__ import True


class countdown_thread:
    
    countThread = None
    running = False
    callback = None
    
    LOST_TIME = 60
    
    def __init__(self, controller, callback=None):
        self.controller = controller
        self.callback = callback
    
    
    def lostNumbersEntered(self):
        if self.running == True:
            print "You did it!  hooray!"
            self.resetCountdown( self.LOST_TIME )
        else:
            print "Nothing was happening - why did you enter the numbers?"

    
    def resetCountdown(self, numSeconds):
        
        # stop previous countdown thread if it was running
        if not self.countThread == None:
            self.stopCounting()
            self.countThread.join(5)

        print "new countdown set to " + str(numSeconds)
        
        # start new countdown thread
        self.countThread = threading.Thread(group=None, target=self.countdownRun, name="countdownThread", args=(numSeconds,), kwargs={})
        self.countThread.start()
        
    def countdownRun(self, numSeconds):
        self.running = True
        
        print "counting down..."
        print "to " + str(numSeconds)
        
        for x in range(0, numSeconds): 
            print "running? " + str(self.isRunning()) + " " + str(x)
            sleep(0.5)
            if self.isRunning() == False:
                break
        
        if not self.callback == None:
            self.callback()
            
        print "Done counting"
        
    def isRunning(self):
        return self.running
        
    def stopCounting(self):
        self.running = False
        
    