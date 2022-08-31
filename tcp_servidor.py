# Para executar no Linux, digite './tcp_servidor.py' no terminal
# Para executar no Windows, digite 'tcp_servidor.py' no Prompt de Comando
# Importando a biblioteca socket
import socket, sys, os,threading
from server_config import *


# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(MAX_LISTEN) # Máximo de conexões enfileiradas
def nonexão():
  while True:
    con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
    cliente = threading.Thread(target=ligar, args=[con,cliente])
    cliente.start()

def ligar(con,cliente):

  try:
    while True:
      
      
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
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU MENSAGENS DO ARQUIVO LOG'
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
 
        #Fazendo pesquisa no Youtube
        elif '\\Y:' in mensagem.upper():
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU UMA PESQUISA NO YOUTUBE'
          arquivoLog(mensagemLog)
          pesquisa = mensagem.split(':',1)          
          con.send(youtube(pesquisa[1]).encode(CODE_PAGE))          
        elif '\\RSS:' in mensagem.upper():
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU UMA PESQUISA DE NOTICIAS'
          arquivoLog(mensagemLog)
          pesquisa = mensagem.split(':',1)          
          con.send(youtube(pesquisa[1]).encode(CODE_PAGE))
        
        elif '\\@:' in mensagem.upper():
          mensagemLog = f'[{date}] {cliente} - CLIENTE SOLICITOU DADOS DE UM USUARIO DO TWITTER'
          arquivoLog(mensagemLog)
          pesquisa = mensagem.split(':',1)          
          con.send(twitter(pesquisa[1]).encode(CODE_PAGE))
          

        else:

        # Devolvendo uma mensagem (echo) ao cliente
          mensagemLog = f'[{date}] {cliente} - {msg.decode(CODE_PAGE)}'
          arquivoLog(mensagemLog)
          msg_retorno =  msg.decode(CODE_PAGE)
          con.send(msg_retorno.encode(CODE_PAGE))
  except:
    
    mensagemLog = f'[{date}] {cliente} - \nERRO: {sys.exc_info()[0]}'
    arquivoLog(mensagemLog)
  
  finally:
   
    mensagemLog = f'[{date}] {cliente} - Finalizando Conexão do Cliente'
    arquivoLog(mensagemLog)
    con.close()

  print(f'\nERRO: {sys.exc_info()[0]}')


def main():
  nonexão()
if __name__ == '__main__':
  main()
