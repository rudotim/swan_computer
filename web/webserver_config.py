#from BaseHTTPServer import BaseHTTPRequestHandler
from http.server import BaseHTTPRequestHandler

from os import curdir, sep
import re
import cgi
import json
#import gamecontroller

# This class will handles any incoming request from the browser 
class webserver_config(BaseHTTPRequestHandler):
        
    #controller = None
    
    #def __init__(self, controller):
    #    self.controller = controller
    #    BaseHTTPRequestHandler.__init__(self)
    #    #super(BaseHTTPRequestHandler, self).__init__()
        
    def setController(self, controller):
        self.controller = controller
        
    # Handler for the GET requests
    def do_GET(self):
        print (self.path)
        if self.path=="/":
            self.path="/index.html"
        
        #if None != re.search('/swan/*', self.path):
        #    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        #    if ctype == 'application/json':
        #        print "Yup, it's json"
        
        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            mimetype = "text/html"
            if None != re.search('/swan/*', self.path):
                ctype = ""
                if self.headers['content-type']:
                    ctype = cgi.parse_header(self.headers['content-type'])
                if ctype == 'application/json':
                    mimetype = "application/json"
                    sendReply = True
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply:
                # Open the static file requested and send it
#                f = open(curdir + sep + "../webroot" + sep + self.path)
                f = open(curdir + sep + "webroot" + sep + self.path, "rb")
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read()))
                f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            
    def do_POST(self):
        print("POST> " + self.path)
        if self.path == "/":
            self.path = "/webroot/index.html"
        
        #if None != re.search('/swan/*', self.path):
        #    ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        #    if ctype == 'application/json':
        #        print "Yup, it's json"
        
        try:
            # Check the file extension required and
            # set the right mime type

            sendReply = False
            if None != re.search('/swan/audio/*', self.path):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                print(pdict)
                
                if ctype == 'application/json':
                    data_string = self.rfile.read(int(self.headers['Content-Length']))
                    #print data_string
                    jsonDict = json.loads( data_string )
                    
                    print (jsonDict)
                    # alarm will have id
                    if 'res' in jsonDict:
                        print ("playing sound: [" + jsonDict['res'] + "]")
                        
                        self.controller.playAudio( jsonDict['res'] )
                    else:
                        print ("Failed to find 'file' in jsonDict")
                    
                    sendReply = True
                    
            elif None != re.search('/swan/video/*', self.path):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'application/json':
                    data_string = self.rfile.read(int(self.headers['Content-Length']))
                    #print data_string
                    jsonDict = json.loads( data_string )
                    
                    if 'res' in jsonDict :
                        # video will have name
                        print ("playing video__: " + jsonDict['res'])
                        self.controller.playVideo( jsonDict['res'] )
                    else:
                        print ("Could not find entry for 'res' in dictionary")
                    sendReply = True            
            if sendReply == True:
                # Open the static file requested and send it
                mimetype = "application/json"
                self.send_response(200, "OK")
                self.send_header('Content-type',mimetype)
                self.end_headers()
                
                jsond = "{ \"success\" : true }"
                self.wfile.write( bytes(jsond, "utf-8") )
                
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
