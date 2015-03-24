import socket
import pdb
import re
import struct
UDP_IP = "127.0.0.1"
UDP_PORT = 3333


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
    

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, # internet
                        socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    
    while True:
        data, addr = sock.recvfrom(1024)
        dct = {}
    
        if data.startswith("#bundle") and "hands/ID-centralXYZ" in data:
            print "found!", data

            try:
                dct = parse(data)
            except ParseError as err:
                print 'err'
            except Exception as err:
                print err
                raise
            print sorted(dct.items())
    
        else:
            if not data.startswith('#bundle'):
                raise Exception('weird data')
            data = ''

            #print 'No hand found'

