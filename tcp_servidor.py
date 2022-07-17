# Importando a biblioteca socket
from posixpath import split
import socket, sys, os
from datetime import datetime
from time import sleep

HOST        = ''      # Definindo o IP do servidor
PORT        = 65000   # Definindo a porta
BUFFER_SIZE = 1024     # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8' # Definindo a página de codificação de caracteres
MAX_LISTEN  = 10       # Definindo o máximo de conexões enfileiradas

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(MAX_LISTEN) # Máximo de conexões enfileiradas

print('Recebendo Mensagens...\n\n')
mensagensLog = ['\n']
date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

#Arquivos e Tamanho 
caminho = os.path.dirname(os.path.abspath(__file__))+'\\server_files'



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
          print(f'\nMandando Ajuda Para {cliente} ...\n')
          mensagem_volta = '\n --Listas de Comando-- \n \\f -- Listar Arquivos \n \\d:nome_arquivo -- Efetua o Download do Arquivo \n \\u:nome_arquivo -- Efetua o Upload do Arquivo \n \\q -- Sair do Cliente \n \\m -- lista Mensagens recebidas pelo servidor \n'                
          con.send(mensagem_volta.encode(CODE_PAGE))
        
        # Mensagem de desconexão 
        elif mensagem.upper() == '\\Q': 
          print(f'\nO {cliente} SE DESCONECTOU DO SERVIDOR...\n')
        
        # Mandando lista de Arquivos 
        elif mensagem.upper() == '\\F':
          
            listArquivos = os.listdir(caminho)
            dictArquivos = {}
            for i in listArquivos:    
              dictArquivos.update({i:os.path.getsize(caminho+'\\'+i)}) 
            arquivosTamanho =''
            for i,j in dictArquivos.items():
              arquivosTamanho = arquivosTamanho+i+';'+str(j)+'\n'
            
            if len(arquivosTamanho) > 0 :
              mensagem_volta = arquivosTamanho
              con.send(mensagem_volta.encode(CODE_PAGE))
            else:
              mensagem_volta = 'Sem Arquivos Disponíveis no Momento'
              con.send(mensagem_volta.encode(CODE_PAGE))
    
        #Mandando Lista de Mensagens 
        elif mensagem.upper() == '\\M':
         
          mensagem_volta = listMensagens
          con.send(mensagem_volta.encode(CODE_PAGE))
        
        # Fazendo Download do Arquivo
        elif '\\D:' in mensagem.upper():
            arquivo = mensagem.split(':',1)
            try:
              a = os.path.getsize(caminho+'\\'+arquivo[1])
              mensagem_volta = str(a)
              con.send(mensagem_volta.encode(CODE_PAGE))             
              print(a)
              print(type(a))
              with open(caminho+'\\'+arquivo[1],'rb') as arq:
                for data in arq:                                   
                  con.send(data)                          
              
                print('Arquivo Enviado')
                arq.close()
            except:                
                con.send(mensagem_volta.encode(CODE_PAGE))
                print('Arquivo Inesistente')


        
        # Fazendo Upload do Arquivo 
        elif '\\U:' in mensagem.upper():
          try:
            arquivo = mensagem.split(':',1)
            data_retorno = con.recv(BUFFER_SIZE)
            msg_retorno  = data_retorno.decode(CODE_PAGE)
            a = int(msg_retorno)

            with open(caminho+'\\'+arquivo[1],'wb') as arq:                
                f = -1                                      
                while f*BUFFER_SIZE <= a:                    
                    data_retorno = con.recv(BUFFER_SIZE)
                    f += 1
                    arq.write(data_retorno)
                    print(f)
                             


                print('Recebido')      
            arq.close()
          except:
            print('Erro no Upload') 
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