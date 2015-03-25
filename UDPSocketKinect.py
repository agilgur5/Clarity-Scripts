import socket
import pdb
import re
import struct
UDP_IP = "127.0.0.1"
UDP_PORT = 3333

zStart = .5555555

class ParseError(Exception):
    pass
    

def parse(data):
    match = re.match(
        r'#bundle(?P<whatisthis>.+?)/hands/ID-centralXYZ(?P<id>.+?),ifff(?P<nums>.*)',
        data)
    if not match:
        raise Exception("Could not parse input data: %s" % repr(data))
    dct['id'] = int(match.groupdict()['id'].encode('hex'), 16)
    
    nums = match.groupdict()['nums'].encode('hex')

    n = match.groupdict()['nums']
    dct['len'] = len(n)
    
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
    for x, l in [(1, 'signx'), (1, "signy"), (1, 'signz')] + [(4, x) for x in '?xyz']:
        if x == 1:
            pass
        elif x == 2:
            try:
                dct[l] = struct.unpack('>h', n[idx : idx+x : 1])
            except:
                #raise
                raise ParseError(str(dct))
        else:
            try:
                dct[l] = struct.unpack('>f', n[idx : idx+x : 1])
            except:
                print dct
                #raise
                raise ParseError(str(dct))
        
        idx += x
        
    
    dct['more'] = n[idx:]

    #dct['?'] = tmp[0]
    #dct['x'] = tmp[1]
    #dct['y'] = tmp[2]
    #dct['z'] = tmp[3]
    return dct

def zStart():

def isStretched():
    if z - zStart > .3:
        return True
    else:
        return False

def isPointing():
    if isStretched(z, zStart) == True and abs(x-xi) < .2 and (y-yi) < .2 and (z-zi) < .2:
        return True
    else:
        return False

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, # internet
                        socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    time.sleep(4)
    dct = parse(data)
    zStart = sorted(dct.items())[2]
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
            sorted_dct = sorted(dct.items())
            output = [sorted_dct] + [isPointing]
            print output
        else:
            if not data.startswith('#bundle'):
                raise Exception('weird data')
            data = ''

            #print 'No hand found'

