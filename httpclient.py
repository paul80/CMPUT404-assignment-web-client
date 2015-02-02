#!/usr/bin/env python
# coding: utf-8
# Copyright 2015 Paul Nhan, Jessica Surya
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

#Original creator: Abram Hindle
#Assignment contributors: Paul Nhan (pnhan), Jessica Surya (jsurya)
#CMPUT 410 Assignment 2 Submission

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
    #print "httpclient.py [URL] [GET/POST]\n"
    
class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    

class HTTPClient(object):
    
    def get_host_port(self,url):
        try:
            remote_address=socket.gethostbyname(url)
            print "IP address of " +url + " is " + remote_address
            return remote_address            
        
        except socket.gaierror:
            print "Hostname couldn't be resolved"
            sys.exit()
            
         
    def connect(self, host, port):
        # use sockets!
        #Create a socket then connect
        try:
            aSocket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print "Socket created"
            
        except socket.error as msg:
            print "Failed to create socket"
            print ("Error code: " +str(msg[0]) + ", Error message: "+msg[1])
            sys.exit()
        
        remote_ip=self.get_host_port(host)
        
        aSocket.connect((remote_ip, port)) 
        print 'Socket Connected to ' + host + ' on ip ' + remote_ip + " by port " +str(port)
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
                port_number=int(port_number)
            else:
                port_number=port_and_path[0:]
                port_number=int(port_number)
                #path=""
        
        else:
            host_and_path=parameters[1][2:]
            if ("/") in host_and_path:
                index= host_and_path.find("/")
                host= host_and_path[:index]
                path=host_and_path[index:]
            else:
                host=host_and_path[0:]
                #path=""
        
        return host,path,port_number
            
    
    def get_code(self, data):
        #Find first \r\n to get status line which has the code
        index= data.find("\r\n")
        fragment= data[0:index]
        fragment=fragment.split(" ")
        code=int(fragment[1])
        return code

    def get_headers(self,data):
        #Find "\r\n\r\n" since it denotes the end of the header
        index=data.find("\r\n\r\n")
        fragment=data[0:index]
        return fragment

    def get_body(self, data):
        index=data.find("\r\n\r\n")
        fragment=data[index:]
        return fragment

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
        #code = 500
        host,path,port= self.get_parameters(url)
        aSocket=self.connect(host,port)
        message= "GET /"+path+" HTTP/1.1\r\nHost: "+host+"\r\nAccept:*/*\r\nConnection:close\r\n\r\n"
        
        #Send to the socket
        try:
            aSocket.sendall(message)
        except socket.error:
            print("Sending data failed")
            sys.exit()
            
        #Get back from the socket using recvall
        #Need to parse the data received back
        data=self.recvall(aSocket) 
        code=self.get_code(data)
                
        header=self.get_headers(data)
        body=self.get_body(data)
        return HTTPRequest(code,body)

    def POST(self, url, args=None):
        #code = 500
        host,path,port= self.get_parameters(url)
        aSocket=self.connect(host,port)
        
        #if there are args, encode it, else args is set to empty string
        if args!=None:
            encoding=urllib.urlencode(args)
        else:
            encoding=''

        message= "POST /"+path+ " HTTP/1.1\r\nHost: "+host+"\r\nAccept: */*\r\nContent-Length: "+str(len(encoding))+"\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n"+encoding
        
        #Send to the socket
        try:
            aSocket.sendall(message)
        except socket.error:
            print("Sending data failed")
            sys.exit()
            
        #Get back from the socket using recvall
        #Need to parse the data received back        
        data=self.recvall(aSocket)
        
        code=self.get_code(data)
        header=self.get_headers(data)
        body=self.get_body(data)
        
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
        
     # Note: The arguments are reversed to comply with project specifications
    elif (len(sys.argv) == 3):
        #print client.command( sys.argv[1], sys.argv[2] )
        print client.command (sys.argv[2],sys.argv[1])
    else:
        #print client.command( command, sys.argv[1] )  
        print client.command(sys.argv[1],command)
