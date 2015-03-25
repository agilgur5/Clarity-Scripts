# George Li, Sagar Vadalia, & Anton Gilgur, with the gracious help of Alex Gaudio

import socket
import pdb
import re
import struct
from time import sleep
from multiprocessing import Process
from multiprocessing import Manager
import SocketServer

UDP_IP, UDP_PORT = "127.0.0.1", 3333
HOST, PORT = "localhost", 9999

class MyTCPHandler(SocketServer.StreamRequestHandler):
    f = open("examplefile.txt", "w")
    def handle(self):
        
        self.write("examplefile.text", "w")
        # self.request is the TCP socket connected to the client
        self.wfile.write(str(items));
        


class ParseError(Exception):
    pass


def parse(data):
    match = re.match(
        r'#bundle(?P<whatisthis>.+?)/hands/ID-centralXYZ(?P<id>.+?),ifff(?P<nums>.*)',
        data)
    if not match:
        raise Exception("Could not parse input data: %s" % repr(data))
    
    nums = match.groupdict()['nums'].encode('hex')

    n = match.groupdict()['nums']
    
    # THIS WORKS e, g, i  == x, y, z
    #idx = 0
    #for x, l in [(2, x) for x in 'abcdefghijklmnop']:
    #    #print l, idx, idx+x, repr(n[idx : idx+x : 1]), repr(n[idx : idx+x : 1].encode('hex'))
    #    #print dct
    #    
    #    try:  # works for e, g, i
    #        dct[l] = int(n[idx : idx+x : 1].encode('hex'), 16)
    #    except:
    #        raise ParseError('')

    # Get x,y,z coordinates as floats.  top left is (0, 0)  bottom right is (1, 1)
    idx = 0
    dct={}
    for x, l in [(1, 'signx'), (1, "signy"), (1, 'signz'), (4, '?')] + [(4, x) for x in 'xyz']:
        if x == 1:
            pass
        elif x == 2:
            pass
        elif l == '?':
            pass
        else:
            try:
                dct[l] = struct.unpack('>f', n[idx : idx+x : 1])
            except:
                print dct
                #raise
                raise ParseError(str(dct))
        
        idx += x
        
    

    #dct['?'] = tmp[0]
    #dct['x'] = tmp[1]
    #dct['y'] = tmp[2]
    #dct['z'] = tmp[3]
    return dct

def receiveUDP(items):
        
    while True:
        data, addr = sock.recvfrom(1024)
        dct = {}
    
        if data.startswith("#bundle") and "hands/ID-centralXYZ" in data:
            #print "found!", data

            try:
                dct = parse(data)
            except ParseError as err:
                print 'err'
            except Exception as err:
                print err
                raise
            
            sorteddict = sorted(dct.items())
            for i in range(len(sorteddict)):
                items[i] = sorteddict[i]
            print items
    
        else:
            if not data.startswith('#bundle'):
                raise Exception('weird data')
            data = ''

            #print 'No hand found'

if __name__ == '__main__':
    manager = Manager()
    items = manager.list([0,0,0]);
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # udp socket
    sock.bind((UDP_IP, UDP_PORT))
    
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    #TCP_IP_IN, TCP_PORT_IN = "tcp://ngrok.com", 46595
    #sock_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tcp socket
    #sock_in.bind((TCP_IP_IN, TCP_PORT_IN))
                
    p = Process(target=receiveUDP, args=[items])
    p.start()
    
    #p2.map(server.serve_forever, [0.25])

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever(0.25)

