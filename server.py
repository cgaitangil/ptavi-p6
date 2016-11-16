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

        # Leyendo línea a línea lo que nos envía el cliente
        line = self.rfile.read()
        petition = line.decode('utf-8')
               
        print('-------------- Petition: -----------------' + '\n')
        print('Client_IP: ' + self.client_address[0])
        print('Client_Port: ' + str(self.client_address[1]))
        print('\n' + "The client sends us: " + petition)
        
        method = petition.split(' ')[0]
        
        Trying = 'SIP/2.0 100 Trying' + '\r\n\r\n'
        Ring = 'SIP/2.0 180 Ring' + '\r\n\r\n'
        OK = 'SIP/2.0 200 OK' + '\r\n\r\n'
        Invite_Res = Trying + Ring + OK # Enviamos los tres paquetes a la vez
        if method == 'INVITE':
            self.wfile.write(bytes(Invite_Res, 'utf-8'))
            print(self.rfile.read().decode('utf-8'))
        elif method == 'BYE':
            self.wfile.write(bytes(OK, 'utf-8'))
        elif method != 'BYE' and method != 'INVITE' and method != 'ACK':
            self.wfile.write(b'SIP/2.0 405 Method Not Allowed\r\n\r\n')
        else:
            self.wfile.write(b'SIP/2.0 400 BAd Request\r\n\r\n')
            
     #   aEjecutar = 'mp32rtp -i ' + str(self.client_address[0]) 
      #  + ' -p ' + str(self.client_address[1]) + petition.split(' ')[-1]
       # os.system(aEjecutar)   
       
        
        
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
        pass
    else:
        sys.exit('\n' + '<' + audio_file + '> File not found.' + '\n')

    serv = socketserver.UDPServer((ServerIP, ServerPort), EchoHandler)
    
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor" + '\n')
