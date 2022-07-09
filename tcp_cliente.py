# Importando a biblioteca socket
from fileinput import close
from pickle import TRUE
import socket

HOST        = 'localhost' # Definindo o IP do servidor
PORT        = 65000       # Definindo a porta
BUFFER_SIZE = 1000000     # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8'     # Definindo a página de codificação de caracteres

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta

while 1:
    msg_pedido = input('Digite a mensagem: ')

    
    # Convertendo a mensagem digitada de string para bytes
    msg = msg_pedido.encode(CODE_PAGE)
    # Enviando a mensagem ao servidor      
    tcp_socket.send(msg)

    # Recebendo echo do servidor
    
    with open('b\\'+msg_pedido,'wb') as arquivo:
        while 1:
            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            arquivo.write(data_retorno)     
    print('Recebido')
arquivo.close()

# Fechando o socket
tcp_socket.close()