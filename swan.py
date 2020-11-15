#!/usr/local/bin/python3

import sys, getopt

#from gamecontroller import gamecontroller
from lost import gamecontroller

from lost.lostengine import lostengine
import traceback

import signal
    
#global sock_comms
#global threadSock
#global lost
sock_comms = None
threadSock = None
lost = None


    
def main( argv ):
    
    global sock_comms
    global threadSock
    global lost
    
    port = 7777
    
    usingPi = False
    cmdString = 'swan.py [-p <port>]'
    try:
        opts, args = getopt.getopt(argv,"h",["pi"])
    except getopt.GetoptError:
        print ('error: {0}'.format(cmdString))
        sys.exit(2)
    for opt, arg in opts:
        print (opt)
        if opt == '-h':
            print ('swan.py [-p <port>]')
            sys.exit()
        elif opt in ("-p"):
            port = opt
        elif opt in ("--pi"):
            usingPi = True
    
    signal.signal(signal.SIGINT, signal_handler)

    #controller = gamecontroller.gamecontroller(usingPi)

    #sock_comms = socket_comms('/tmp/uds_socket', controller);
    #threadSock = Thread(target=sock_comms.start, args=[])
    #threadSock.start()

    #lost = lostengine(controller, quitApp );
    #lost.init( usingPi )


    #threadUI = Thread(target=lost.init, args=[ usingPi ])
    #threadUI.start()

    try:
        controller = gamecontroller.gamecontroller(usingPi)
         
         # start web server in separate thread
         #server = webserver(port, controller)
         #thread = Thread(target = server.start, args = [])
         #thread.start()
         
         #sock_comms = socket_comms( '/tmp/uds_socket' );
         #threadSock = Thread(target = sock_comms.start, args = [])
         #threadSock.start()
        lost = lostengine( controller, quitApp )
        print("start it")
        lost.init( usingPi )
        #threadUI = Thread(target = lost.init, args = [ usingPi ])
        #threadUI.start()


         # start lost engine
         #lost = lostengine(controller)
         #lost.init( usingPi )
         #lost.mainLoop()
         
    except Exception as e:
        tb = traceback.format_exc()
        print ('^C received, shutting down the web server: ', tb)
         #sock_comms.stop()
         #threadSock.join()
    #threadSock.join()
    #threadUI.join()
         #server.stop()
         #thread.join()


def signal_handler(sig, frame):
    print("CTRL-C")
    
    lost.stop()
    
    quitApp()


def quitApp():
    print("quitting")
    sock_comms.stop()
    threadSock.join()
    print("socket done");
        
    #threadUI.join()
    #server.stop()
    #thread.join()

if __name__ == "__main__":
    main(sys.argv[1:])
