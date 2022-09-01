# Importando a biblioteca socket

import socket,os,tqdm
from time import sleep

HOST        = 'localhost' # Definindo o IP do servidor
PORT        = 65000       # Definindo a porta
BUFFER_SIZE = 4096         # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8'     # Definindo a página de codificação de caracteres

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta

caminho = os.path.dirname(os.path.abspath(__file__))+'\\client_files'

while True:
    mensagem = input('Digite a mensagem (\h -- Ajuda): \n')
    
    # Convertendo a mensagem digitada de string para bytes
    msg = mensagem.encode(CODE_PAGE)
    # Enviando a mensagem ao servidor      
    tcp_socket.send(msg)
   
    if msg.decode(CODE_PAGE).upper() == '\Q': break
    elif '\\D:' in mensagem.upper():
        try:
            arquivo = mensagem.split(':',1)
            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            msg_retorno  = data_retorno.decode(CODE_PAGE)
            filesize = int(msg_retorno)               
            with open(caminho+'\\'+arquivo[1],'wb') as arq:             
                while 1:                        
                    data_retorno = tcp_socket.recv(BUFFER_SIZE)
                    arq.write(data_retorno)
                    sleep(0.0001)                                             
                    if len(data_retorno)<BUFFER_SIZE:break
            print('Recebido')      
            
        except:
            print('Erro no download') 
                
    elif '\\U:' in mensagem.upper():
        arquivo = mensagem.split(':',1)
        print(arquivo[1])
        with open(caminho+'\\'+arquivo[1],'rb') as arq:
                for data in arq:                                   
                        tcp_socket.send(data)
                print('enviado')                        
        arq.close()
      

    else:
        # Recebendo echo do servidor
            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            msg_retorno  = data_retorno.decode(CODE_PAGE)
            print(f'{msg_retorno}')

# Fechando o socket
tcp_socket.close()