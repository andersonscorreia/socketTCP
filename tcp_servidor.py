# Importando a biblioteca socket
from posixpath import split
import socket, sys, os
from datetime import datetime

HOST        = ''      # Definindo o IP do servidor
PORT        = 65000   # Definindo a porta
BUFFER_SIZE = 1024      # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8' # Definindo a página de codificação de caracteres
MAX_LISTEN  = 10       # Definindo o máximo de conexões enfileiradas

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(MAX_LISTEN) # Máximo de conexões enfileiradas

print('Recebendo Mensagens...\n\n')
mensagensLog = ['\n']
data = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

#Arquivos e Tamanho 
caminho = os.path.dirname(os.path.abspath(__file__))+'\\server_files'
listArquivos = os.listdir(caminho)
dictArquivos = {}
for i in listArquivos:    
    dictArquivos.update({i:os.path.getsize(caminho+'\\'+i)}) 
arquivosTamanho =''
for i,j in dictArquivos.items():
    arquivosTamanho = arquivosTamanho+i+';'+str(j)+'\n'

try:
  while True:
    con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    print('Conectado por: ', cliente)
    while True:
        msg = con.recv(BUFFER_SIZE) #buffer de 1024 bytes
        mensagem = msg.decode(CODE_PAGE)
        
        mensagensLog.append(data+'; '+cliente[0]+'; '+mensagem+'\n')
        
        listMensagens = '\n --Lista de Mensagens-- \n'
        
        for i in mensagensLog:
          listMensagens += i
        # Mandando Ajuda 
        if mensagem.upper() == '\\H':
          print(f'\nMandando Ajuda Para {cliente} ...\n')
          mensagem_volta = '\n --Listas de Comando-- \n \\f -- Listar Arquivos \n \\d:nome_arquivo -- Efetua o Download do Arquivo \n \\u:nome_arquivo -- Efetua o Upload do Arquivo \n \\q -- Sair do Cliente \n'                
          con.send(mensagem_volta.encode(CODE_PAGE))
        
        # Mensagem de desconexão 
        elif mensagem.upper() == '\\Q': 
          print(f'\nO {cliente} SE DESCONECTOU DO SERVIDOR...\n')
        
        # Mandando lista de Arquivos 
        elif mensagem.upper() == '\\F':
          mensagem_volta = arquivosTamanho
          con.send(mensagem_volta.encode(CODE_PAGE))
        
        #Mandando Lista de Mensagens 
        elif mensagem.upper() == '\\M':
          print(f'\n Efetua o Upload do Arquivo... {cliente} ...\n')
          mensagem_volta = listMensagens
          con.send(mensagem_volta.encode(CODE_PAGE))
        
        # Fazendo Download do Arquivo
        elif '\\D:' in mensagem.upper():
            arquivo = mensagem.split(':',1)
            try:
              with open(caminho+'\\'+arquivo[1],'rb') as arquivo:
                for data in arquivo:                  
                  con.send(data)                           
                print('Arquivo Enviado')
            except:
                print('Arquivo Inesistente')


        
        # Fazendo Upload do Arquivo 
        elif '\\U:' in mensagem.upper():
            print(f'\n Efetua o Upload do Arquivo... {cliente} ...\n')
            mensagem_volta = '\nAinda em Construção... '
            con.send(mensagem_volta.encode(CODE_PAGE))

        else:
        # Imprimindo a mensagem recebida convertendo de bytes para string
          print(cliente, msg.decode(CODE_PAGE))
        # Devolvendo uma mensagem (echo) ao cliente
          msg_retorno = 'Devolvendo...' + msg.decode(CODE_PAGE)
          con.send(msg_retorno.encode(CODE_PAGE))
except:
  print(f'\nERRO: {sys.exc_info()[0]}')
finally: 
   print('Finalizando Conexão do Cliente ', cliente)
   con.close()