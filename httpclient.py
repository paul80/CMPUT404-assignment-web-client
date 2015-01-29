#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re

# you may use urllib to encode data appropriately
import urllib

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    

class HTTPClient(object):
    
    def get_host_port(self,url):
        try:
            remote_address=socket.gethostbyname(url)
            print "IP address of" +url + " is " + remote_address
            return remote_address            
        
        except socket.gaierror:
            print "Hostname couldn't be resolved"
            sys.exit()
            
         
    def connect(self, host, port):
        # use sockets!
        #Create a socket first
        try:
            aSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "Socket created"
            
        except socket.error as msg:
            print "Failed to create socket"
            print ("Error code: " +str(msg[0]) + ", Error message: "+msg[1])
            sys.exit()
        
        remote_ip=self.get_host_port(host)
        
        aSocket.connect((remote_ip, port))       
        return aSocket

    # http://www.example.com:8080/path/
    #When split by ":"
    #Get ['http', '//www.example.com', '8080/path/']
    def get_parameters(self,url):
        
        if ("http://") not in url:
            url="http://"+url
            
        parameters= url.split(":")
        host=""
        port_number=80
        path=""
        
        if (len(parameters))>2:
            #There is a port number
            host= parameters[1][2:]
            port_and_path=parameters[-1]
            
            if ("/") in port_and_path:
                index= port_and_path.find("/")
                port_number= port_and_path[0:index]
                path=port_and_path[index:]
            else:
                port_number=port_and_path[0:]
                path="/"
        
        else:
            host_and_path=parameters[1][2:]
            if ("/") in host_and_path:
                index= host_and_path.find("/")
                host= host_and_path[:index]
                path=host_and_path[index:]
            else:
                host=host_and_path[0:]
                path="/"
        
        print "Host is " +host
        print "Path is " +path
        print "Port number is " +str(port_number)
        
        return host,path,port_number
            
    
    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    def GET(self, url, args=None):
        code = 500
        print "URL is " +url
        #ip_address= self.get_host_port(url)
        #host= socket.gethostbyaddr(ip_address)
        host,path,port= self.get_parameters(url)
        aSocket=self.connect(host,port)
        
        body = "GET / HTTP/1.1\r\nUser-Agent: \r\nHost: \r\nAccept: */*\r\n \r\n"
        #Print out to stdout
        print("GOT TO GET METHOD")
        print body
        
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = "POST / HTTP/1.1\r\nUser-Agent: \r\nHost: \r\nAccept: */*\r\n \r\n"
        print body
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[1], sys.argv[2] )
    else:
        print client.command( command, sys.argv[1] )    
