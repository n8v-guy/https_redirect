#!/usr/bin/python
"""Simple transparent HTTP to HTTPS redirect script to force SSL connection"""

import socket, sys

__author__  = "Max Shashkov"
__license__ = "The MIT License (MIT)"

if len(sys.argv) < 2:
    print(__doc__)
    print('Usage: ' + sys.argv[0] + ' example.com 80')
    print('   or: nohup ' + sys.argv[0] + ' example.com 80 &')
    sys.exit()

host = sys.argv[1]
port = 80 if len(sys.argv) == 2 else int(sys.argv[2])

print('Serving redirects to https from port ' + str(port) + '\n'
      'Press Control+C for interrupting')
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', port))
sock.listen(5)  # default queue size on most systems

while True:
    try:
        connection, _ = sock.accept()
        path = connection.recv(1024).split(' ')[1]  # skip GET, get path
        connection.sendall('HTTP/1.1 301 Moved Permanently\n'
                           'Location: https://' + host + path + '\n' +
                           '\n' +
                           'Redirecting to https version of ' + host)
        connection.close()
    except KeyboardInterrupt:
        break
