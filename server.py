#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os.path 

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")

        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        petition = line.decode('utf-8')
        print('-------------- Petition: -----------------' + '\n')
        print(petition)
        print("El cliente nos manda: " + petition)

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    try:
        ServerIP = sys.argv[1]
        ServerPort = int(sys.argv[2])
        fich = sys.argv[3]
    except:
        Error = 'Usage: python3 server.py IP port audio_file'
        sys.exit('\n' + Error + '\n')
        
    # Comprobamos si existe el fichero pasado al lanzar el servidor
    if os.path.isfile(fich):
        pass
    else:
        sys.exit('\n' + fich + ' not found' + '\n')

    serv = socketserver.UDPServer((ServerIP, ServerPort), EchoHandler)
    print('')
    print("Lanzando servidor UDP de eco...")
    print('')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor" + '\n')
