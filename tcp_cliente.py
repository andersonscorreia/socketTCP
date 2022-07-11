# Importando a biblioteca socket
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
            arquivo = mensagem.split(':',1)
            with open(caminho+'\\'+arquivo[1],'wb') as arquivo:
                while 1:
                    data_retorno = tcp_socket.recv(BUFFER_SIZE)
                    if not data_retorno:break
                    arquivo.write(data_retorno)     
                print('Recebido')
    else:
        # Recebendo echo do servidor
            data_retorno = tcp_socket.recv(BUFFER_SIZE)
            msg_retorno  = data_retorno.decode(CODE_PAGE)
            print(f'Echo Recebido: {msg_retorno}')

# Fechando o socket
tcp_socket.close()