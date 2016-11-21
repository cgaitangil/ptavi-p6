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

    REC_IP = LINE[1][LINE[1].find('@') + 1:LINE[1].find(':')]
    REC_PORT = int(LINE[1][LINE[-1].find(':') + 1:])
    REC_NAME = LINE[1][:LINE[1].find('@')]

    LINE = LINE[0].upper() + ' sip:' + LINE[1][:-5] + ' SIP/2.0\r\n\r\n'

except:
    Error = 'Usage: python3 client.py method receiver@IP:SIPport'
    sys.exit('\n' + Error + '\n')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((REC_IP, REC_PORT))

print('\n' + "Sending: " + LINE)
my_socket.send(bytes(LINE, 'utf-8'))

response = my_socket.recv(1024).decode('utf-8')

print('Received:' + '\n' + response)

# Enviamos ACK si recibimos el paquete con las cabeceras Trying, Ring y OK.
ack = 'ACK sip:' + REC_NAME + '@' + REC_IP + ' SIP/2.0'
if response.split('\r\n\r\n')[0] == 'SIP/2.0 100 Trying':
    print('Sending ACK (Trying Response) --> ' + ack)
    my_socket.send(bytes(ack, 'utf-8'))
print('\nFinished Socket.\n')

# Cerramos todo
my_socket.close()
