#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.



# Contenido que vamos a enviar

try:
    LINE = sys.argv[1:]
    LINE = LINE[0].upper() + ' ' + LINE[1]
    LIST = LINE.split(' ')

    # Dirección IP del servidor.
    SERVER = LIST[-1][LIST[-1].find('@') + 1:LIST[-1].find(':')]
    PORT = int(LIST[-1][LIST[-1].find(':') + 1:])

except:
    Error = 'Usage: python3 client.py method receiver@IP:SIPport'
    sys.exit('\n' + Error + '\n')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print('')

print("Sending: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Received:' + '\n' + data.decode('utf-8'))
print("Ending socket..." + '\n')

# Cerramos todo
my_socket.close()
