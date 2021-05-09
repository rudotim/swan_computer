#!/usr/local/bin/python3

import sys
import getopt

from threading import Thread

from lost import lost_controller

from ui.ui_engine import UIEngine
import traceback

import signal

from web.webserver import webserver


class Swan:

    def __init__(self, argv):

        self.controller = None
        self.server = None
        self.lost = None

        self.port = 7777

        self.using_pi = False
        self.parse_parameters(argv)


    def parse_parameters(self, argv):
        cmd_string = 'swan.py [-p <port>]'
        try:
            opts, args = getopt.getopt(argv, "h", ["pi"])
        except getopt.GetoptError:
            print('error: {0}'.format(cmd_string))
            sys.exit(2)
        for opt, arg in opts:
            print(opt)
            if opt == '-h':
                print('swan.py [-p <port>] --pi')
                sys.exit()
            elif opt in "-p":
                self.port = opt
            elif opt in "--pi":
                print("Using raspberry pi")
                self.using_pi = True

    def start(self):
        #sock_comms = socket_comms('/tmp/uds_socket', controller);
        #threadSock = Thread(target=sock_comms.start, args=[])
        #threadSock.start()

        #threadUI = Thread(target=lost.init, args=[ using_pi ])
        #threadUI.start()

        try:
            self.controller = lost_controller.LostController(self.using_pi)

            # start web server in separate thread
            self.server = webserver(self.port, self.controller)
            thread = Thread(target=self.server.start, args=[])
            thread.start()

            #sock_comms = socket_comms( '/tmp/uds_socket' );
            #threadSock = Thread(target = sock_comms.start, args = [])
            #threadSock.start()

            # start lost UI engine
            self.lost = UIEngine(self.controller, self.quit_app)
            self.lost.init(self.using_pi)

            #threadUI = Thread(target = lost.init, args = [ using_pi ])
            #threadUI.start()


        except Exception as e:
            tb = traceback.format_exc()
            print('^C received, shutting down the web server: ', tb)
            #sock_comms.stop()
            #threadSock.join()
            #threadSock.join()
            #threadUI.join()
            #server.stop()
            #thread.join()

    def quit_app(self, ctrl_c=False):
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
    swan.quit_app(True)


if __name__ == "__main__":
    swan = Swan(sys.argv[1:])
    signal.signal(signal.SIGINT, signal_handler)
    swan.start()
