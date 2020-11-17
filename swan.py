#!/usr/local/bin/python3

import sys, getopt

#from gamecontroller import gamecontroller
from lost import gamecontroller

from lost.swanengine import SwanEngine
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
    
    using_pi = False
    cmd_string = 'swan.py [-p <port>]'
    try:
        opts, args = getopt.getopt(argv, "h", ["pi"])
    except getopt.GetoptError:
        print('error: {0}'.format(cmd_string))
        sys.exit(2)
    for opt, arg in opts:
        print (opt)
        if opt == '-h':
            print('swan.py [-p <port>]')
            sys.exit()
        elif opt in "-p":
            port = opt
        elif opt in "--pi":
            using_pi = True
    
    signal.signal(signal.SIGINT, signal_handler)

    #controller = gamecontroller.gamecontroller(using_pi)

    #sock_comms = socket_comms('/tmp/uds_socket', controller);
    #threadSock = Thread(target=sock_comms.start, args=[])
    #threadSock.start()

    #lost = lostengine(controller, quitApp );
    #lost.init( using_pi )


    #threadUI = Thread(target=lost.init, args=[ using_pi ])
    #threadUI.start()

    try:
        controller = gamecontroller.gamecontroller(using_pi)
         
         # start web server in separate thread
         #server = webserver(port, controller)
         #thread = Thread(target = server.start, args = [])
         #thread.start()
         
         #sock_comms = socket_comms( '/tmp/uds_socket' );
         #threadSock = Thread(target = sock_comms.start, args = [])
         #threadSock.start()
        lost = SwanEngine(controller, quitApp)
        print("start it")
        lost.init( using_pi )
        #threadUI = Thread(target = lost.init, args = [ using_pi ])
        #threadUI.start()


         # start lost engine
         #lost = lostengine(controller)
         #lost.init( using_pi )
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
