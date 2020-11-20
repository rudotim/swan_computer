'''
Created on Oct 21, 2018

@author: tim
'''
import socket
import os
  
  

    
class socket_comms:
    
    MESSAGE_SEPARATOR = chr(4)
    BUFFLEN = 16
    
    def __init__(self, socket_path, controller ):
        self.server_address = socket_path
        self.sock = None
        self.controller = controller
        print ("init socket_comms on sockysock path: " + self.server_address)
 
    def start(self):
        # Make sure the inet_socket does not already exist
        try:
            os.unlink(self.server_address)
        except OSError:
            if os.path.exists(self.server_address):
                raise
        
        # Create a UDS inet_socket
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    
        # Bind the inet_socket to the port
        #print >>sys.stderr, 'starting up on %s' % self.server_address
        print("starting up on ", self.server_address)
        self.sock.bind(self.server_address)
        
        # Listen for incoming connections
        self.sock.listen(1)

        connection = None
        client_address = None
            
        while True:
            # Wait for a connection
            print("waiting for a connection...")
            try:
                connection, client_address = self.sock.accept()
            except ConnectionAbortedError:
                print("socket.accept closed")
                break
                
            try:
                print("got connection from ", client_address)
        
                chunks = []
                # Receive the data in small chunks and retransmit it
                while True:
                    
                    data = connection.recv(self.BUFFLEN)
                        
                    if not data:
                        print("no more data from ", client_address)
                        break
    
                    print("data>", data)
                    data = data.decode('utf-8')
                    #print("stringdata> ", stringdata)
                    terminatingIndex = data.find( self.MESSAGE_SEPARATOR ) 
                    if terminatingIndex >= 0:
                        chunks.append( data[:terminatingIndex] )
                        fullMesage = ''.join(chunks)
                        print("full>", fullMesage)
                        self.controller.receiveText( fullMesage )
                        # reset
                        chunks = []
                    else:                
                        chunks.append( data )                    
                        
            finally:
                # Clean up the connection
                if connection != None:
                    connection.close()
            
    def stop(self):
        print("stopping socket_comms")
        #self.sock.shutdown(socket.SHUT_WR)
        self.sock.close()