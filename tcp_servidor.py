# Importando a biblioteca socket
import socket, sys, os
from server_config import *


# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(MAX_LISTEN) # Máximo de conexões enfileiradas

print('Recebendo Mensagens...\n\n')


try:
  while True:
    con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    print('Conectado por: ', cliente)
    while True:
        msg = con.recv(BUFFER_SIZE) #buffer de 1024 bytes
        mensagem = msg.decode(CODE_PAGE)        
        mensagensLog.append(date+'; '+cliente[0]+'; '+mensagem+'\n')        
        listMensagens = '\n --Lista de Mensagens-- \n'        
        for i in mensagensLog:
          listMensagens += i
        # Mandando Ajuda 
        if mensagem.upper() == '\\H':
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU AJUDA'
          arquivoLog(mensagemLog)
          ajuda(CODE_PAGE,con)
                  

        
        # Mensagem de desconexão 
        elif mensagem.upper() == '\\Q': 
          mensagemLog = f'[{date}] {cliente} - SE DESCONECTOU DO SERVIDOR'
          arquivoLog(mensagemLog)
        
        # Mandando lista de Arquivos 
        elif mensagem.upper() == '\\F':
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU A LISTA DE ARQUIVOS DISPONIVEIS'
          arquivoLog(mensagemLog)
          listArquivos(con,caminhoServer)          

        #Mandando Lista de Mensagens 
        elif mensagem.upper() == '\\M':
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU A LISTA DE ARQUIVOS DISPONIVEIS'
          arquivoLog(mensagemLog)
          mensagens(con,caminhoLog)
          
        
        # Fazendo Download do Arquivo
        elif '\\D:' in mensagem.upper():
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU DOWNLOAD DE ARQUIVO'
          arquivoLog(mensagemLog)
          download(mensagem,con,caminhoServer)

        
        # Fazendo Upload do Arquivo 
        elif '\\U:' in mensagem.upper():
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU UPLOAD DE ARQUIVO'
          arquivoLog(mensagemLog)
          upload(caminhoServer,con,mensagem)
 
        else:

        # mensagem recebida convertendo de bytes para string
          recebida = (cliente, msg.decode(CODE_PAGE))
        # Devolvendo uma mensagem (echo) ao cliente
          mensagemLog = f'[{date}] {cliente} - {msg.decode(CODE_PAGE)}'
          arquivoLog(mensagemLog)
          msg_retorno =  msg.decode(CODE_PAGE)
          con.send(msg_retorno.encode(CODE_PAGE))
except:
  print(f'\nERRO: {sys.exc_info()[0]}')
finally: 
   print('Finalizando Conexão do Cliente ', cliente)
   con.close()