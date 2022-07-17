# Importando a biblioteca socket
from calendar import c
from fileinput import close
import socket,os

HOST        = 'localhost' # Definindo o IP do servidor
PORT        = 65000       # Definindo a porta
BUFFER_SIZE = 1024         # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8'     # Definindo a página de codificação de caracteres

# Criando o socket UDP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.connect((HOST, PORT)) # Ligando o socket a porta

caminho = os.path.dirname(os.path.abspath(__file__))+'\\client_files'

while True:
    mensagem = input('Digite a mensagem (\h -- Ajuda): ')
    
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
            a = int(msg_retorno)            
            with open(caminho+'\\'+arquivo[1],'wb') as arq:                
                f = -1                                      
                while f*BUFFER_SIZE <= a:
                    data_retorno = tcp_socket.recv(BUFFER_SIZE)
                    arq.write(data_retorno)
                    print()
                    f += 1          
            arq.close()
            print('Recebido')
             
        except:
            print('Erro no download')
    elif '\\U:' in mensagem.upper():
            arquivo = mensagem.split(':',1)
            try:
              a = os.path.getsize(caminho+'\\'+arquivo[1])
              mensagem_volta = str(a)
              tcp_socket.send(mensagem_volta.encode(CODE_PAGE))             
              print(a)
              print(type(a))
              with open(caminho+'\\'+arquivo[1],'rb') as arquivo:
                for data in arquivo:                                   
                  tcp_socket.send(data)                          
              
                print('Arquivo Enviado')
            except:
                mensagem_volta = 'Erro no download '
                tcp_socket.send(mensagem_volta.encode(CODE_PAGE))
                print('Arquivo Inesistente')
    
    
    else:
        # Recebendo echo do servidor
            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            msg_retorno  = data_retorno.decode(CODE_PAGE)
            print(f'Echo Recebido: {msg_retorno}')

# Fechando o socket
tcp_socket.close()