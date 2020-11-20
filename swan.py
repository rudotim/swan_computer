#!/usr/local/bin/python3

import sys, getopt

#from gamecontroller import gamecontroller
from threading import Thread

from lost import gamecontroller

from lost.swanengine import SwanEngine
import traceback

import signal

from web.webserver import webserver


class Swan:

    def __init__(self, argv):

        self.parse_parameters(argv)

        self.controller = None
        self.server = None
        self.lost = None

        self.port = 7777

        self.using_pi = False

    def parse_parameters(self, argv):
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

    def start(self):
        #controller = gamecontroller.gamecontroller(using_pi)

        #sock_comms = socket_comms('/tmp/uds_socket', controller);
        #threadSock = Thread(target=sock_comms.start, args=[])
        #threadSock.start()

        #lost = lostengine(controller, quitApp );
        #lost.init( using_pi )


        #threadUI = Thread(target=lost.init, args=[ using_pi ])
        #threadUI.start()

        try:
            self.controller = gamecontroller.gamecontroller(self.using_pi)

            #start web server in separate thread
            self.server = webserver(self.port, self.controller)
            thread = Thread(target=self.server.start, args=[])
            thread.start()

            #sock_comms = socket_comms( '/tmp/uds_socket' );
            #threadSock = Thread(target = sock_comms.start, args = [])
            #threadSock.start()
            self.lost = SwanEngine(self.controller, self.quitApp)
            self.lost.init(self.using_pi)
            #threadUI = Thread(target = lost.init, args = [ using_pi ])
            #threadUI.start()


             # start lost engine
             #lost = lostengine(controller)
             #lost.init( using_pi )
             #lost.mainLoop()

        except Exception as e:
            tb = traceback.format_exc()
            print('^C received, shutting down the web server: ', tb)
             #sock_comms.stop()
             #threadSock.join()
        #threadSock.join()
        #threadUI.join()
             #server.stop()
             #thread.join()

    def quitApp(self, ctrl_c=False):
        print("quitApp")
        if ctrl_c:
            self.lost.stop()
        #sock_comms.stop()
        #threadSock.join()
        print("socket done")
        self.server.stop()

        #threadUI.join()
        #server.stop()
        #thread.join()


swan = None

def signal_handler(sig, frame):
    print("CTRL-C")
    swan.quitApp(True)


if __name__ == "__main__":
    swan = Swan(sys.argv[1:])
    signal.signal(signal.SIGINT, signal_handler)
    swan.start()
