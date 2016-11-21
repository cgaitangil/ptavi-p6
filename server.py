#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path  # Paquete usado para comprobar si existe el archivo mp3
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        Client_IP = self.client_address[0]
        Client_Port = self.client_address[1]

        # Leyendo línea a línea lo que nos envía el cliente
        data = self.rfile.read().decode('utf-8')

        Trying = 'SIP/2.0 100 Trying' + '\r\n\r\n'
        Ring = 'SIP/2.0 180 Ring' + '\r\n\r\n'
        OK = 'SIP/2.0 200 OK' + '\r\n\r\n'
        Invite_Res = Trying + Ring + OK  # Enviamos los tres paquetes a la vez

        method = data.split(' ')[0]
        if method == 'INVITE':
            print('The client sends us: ' + data)
            self.wfile.write(bytes(Invite_Res, 'utf-8'))
            print('Sending:\r\n' + Invite_Res)
        elif method == 'BYE':
            print('The client sends us: ' + data)
            self.wfile.write(bytes(OK, 'utf-8'))
            print('Sending:\r\n' + OK)
            print('\n---------- Next Petition: -----------\n')
        elif method == 'ACK':
            print('Assent: ' + data)

            aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + audio_file
            os.system(aEjecutar)
            print('\nSending ' + audio_file + ' --> ' + aEjecutar)

            print('\n---------- Next Petition: -----------\n')
        elif method != 'BYE' and method != 'INVITE' and method != 'ACK':
            print('The client sends us: ' + data)
            self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
        else:
            print('The client sends us: ' + data)
            self.wfile.write(b'SIP/2.0 400 BAd Request\r\n\r\n')

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        ServerIP = sys.argv[1]
        ServerPort = int(sys.argv[2])
        audio_file = sys.argv[3]
    except:
        Error = 'Usage: python3 server.py IP port audio_file'
        sys.exit('\n' + Error + '\n')

    # Comprobamos si existe el fichero pasado al lanzar el servidor
    if os.path.isfile(audio_file):
        print('\n' + 'Listening...' + '\n')
    else:
        sys.exit('\n' + '<' + audio_file + '> File not found.' + '\n')

    serv = socketserver.UDPServer((ServerIP, ServerPort), EchoHandler)

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor" + '\n')
