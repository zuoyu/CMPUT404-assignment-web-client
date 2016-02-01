#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# Copyright 2016 Yu Zuo
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
    print "httpclient.py [URL] [GET/POST]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body


class HTTPClient(object):
    def get_host_path_port(self,url):
        port = 80
        host =url.replace('http://', "")
        path = "/"


        index1 = host.find('/')
        if index1 != -1:
            path = host[index1:]
            host = host[:index1]


        index2 = host.find(':')
        if index2 != -1:
            port = int(host[index2+1:])
            host = host[:index2]
        return host, path, port

    def connect(self, host, port):
        #create a new socket
        try:
            self.socketclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except soccket.error as msg:
            print('Failed to create socket!')
            sys.exit()

        if (host[-1]== '/'):
            host = host[:-1]

        self.socketclient.connect((host, port))
        return self.socketclient

    def get_code(self, data):
        newdata= data.split()
	code = newdata[1]
        return int(code)

    def get_headers(self,data):
	new_data = data.split('\r\n\r\n')
	header = new_data[0]
        return header
    def get_body(self, data):

        index = data.find('\r\n\r\n')
        body = data[index:]
        return body

    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(24)
            if (part):
                buffer.extend(part)
            else:
                done = not part          
        return str(buffer)

    def GET(self, url, args=None):
        host, path, port = self.get_host_path_port(url)

        request ="GET "+path+" HTTP/1.1 \r\nHost: "+host+"\r\nAccept: */*\r\nConnection:close\r\n\r\n"

        self.clientSocket = self.connect(host,port)
        
        try:
            self.clientSocket.sendall(request.encode("UTF8"))
        except self.clientSocket as msg:
            print('Error code: ' + str(msg[0]) + ', error message: ' + msg[1])
            sys.exit()

        data = self.recvall(self.clientSocket)
        code =self.get_code(data)
        body= self.get_body(data)
        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        host, path, port = self.get_host_path_port(url)
        if args != None:
            args=urllib.urlencode(args)
        else:
            args = ''

        request ="POST "+path+" HTTP/1.1 \r\nHost: "+host+"\r\nContent-Length: "+str(len(args))+"\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept: */*\r\nConnection:close\r\n\r\n"+args

	self.clientSocket = self.connect(host,port)
        
        try:
            self.clientSocket.sendall(request.encode("UTF8"))
        except self.clientSocket as msg:
            print('Error code: ' + str(msg[0]) + ', error message: ' + msg[1])
	    sys.exit()

        data = self.recvall(self.clientSocket)

        code =self.get_code(data)
        body= self.get_body(data)

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
