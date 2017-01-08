from BaseHTTPServer import BaseHTTPRequestHandler
from os import curdir, sep
import re
import cgi
import json

# This class will handles any incoming request from the browser 
class webserver_config(BaseHTTPRequestHandler):
    
    # Handler for the GET requests
    def do_GET(self):
        print self.path
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
            if None != re.search('/swan/*', self.path):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'application/json':
                    print "Yup, it's json"
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

            if sendReply == True:
                # Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            
    def do_POST(self):
        print "POST> " + self.path
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
            if None != re.search('/swan/*', self.path):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'application/json':
                    print "Yup, it's json"
                    mimetype = "application/json"
                    data_string = self.rfile.read(int(self.headers['Content-Length']))
                    print data_string
                    dict = json.loads( data_string )
                    print dict
                    print dict['name']
                    print dict['location']
                    sendReply = True
            
            if sendReply == True:
                # Open the static file requested and send it
                self.send_response(200, "OK")
                self.send_header('Content-type',mimetype)
                self.end_headers()
                
                jsond = "{ \"potato\" : 9 }"
                self.wfile.write( jsond )
                
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
            