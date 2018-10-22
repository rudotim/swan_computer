
from web.webserver_config import webserver_config

#from BaseHTTPServer import HTTPServer
from http.server import HTTPServer

class webserver:
    
    server = None
    
    def __init__(self, port, controller):
        print ("init webserver on port: " + str(port))
        self.port = port
        self.controller = controller
        
    def start(self):
        cfg = webserver_config
        cfg.controller = self.controller
        
        #cfg.setController( self.controller )
        
        # Create a web server and define the handler to manage the
        # incoming request
        self.server = HTTPServer(('', self.port), cfg )
        print ('Started httpserver on port ' , self.port)
        
        # Wait forever for incoming htto requests
        self.server.serve_forever()
        
        
    def stop(self):
        print ("stopping web server")
        if self.server != None:
            self.server.shutdown()
        