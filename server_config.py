import sys, os
from datetime import datetime
from time import sleep

HOST        = ''      # Definindo o IP do servidor
PORT        = 65000   # Definindo a porta
BUFFER_SIZE = 1024     # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8' # Definindo a página de codificação de caracteres
MAX_LISTEN  = 10       # Definindo o máximo de conexões enfileiradas

mensagensLog = ['\n']
date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

caminho = os.path.dirname(os.path.abspath(__file__))+'\\server_files'

def ajuda(CODE_PAGE,con):
        mensagem_volta = '\n --Listas de Comando-- \n \\f -- Listar Arquivos \n \\d:nome_arquivo -- Efetua o Download do Arquivo \n \\u:nome_arquivo -- Efetua o Upload do Arquivo \n \\q -- Sair do Cliente \n \\m -- lista Mensagens recebidas pelo servidor \n'                
        con.send(mensagem_volta.encode(CODE_PAGE))


def listArquivos(con,caminho):
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

def mensagens(con,listMensagens):
        mensagem_volta = listMensagens
        con.send(mensagem_volta.encode(CODE_PAGE))

def download(mensagem,con,caminho):
        arquivo = mensagem.split(':',1)
        try:
              a = os.path.getsize(caminho+'\\'+arquivo[1])
              mensagem_volta = str(a)
              con.send(mensagem_volta.encode(CODE_PAGE))             
    
              with open(caminho+'\\'+arquivo[1],'rb') as arq:
                for data in arq:                                   
                  con.send(data)                          
              
                sleep(0.001)
                
        except:
                mensagem_volta = 'Arquivo Inesistente'
                con.send(mensagem_volta.encode(CODE_PAGE))                
              
                
        arq.close()

def upload(caminho,con,mensagem):
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
                    sleep(0.001)                            


                  
            
        except:
                mensagem_volta = f'\nERRO: {sys.exc_info()[0]}'
                con.send(mensagem_volta.encode(CODE_PAGE))                
              
                
        



