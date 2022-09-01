from fileinput import close
import sys, os, requests,feedparser,json
from datetime import datetime
from time import sleep


HOST        = ''      # Definindo o IP do servidor
PORT        = 65000    # Definindo a porta
BUFFER_SIZE = 4096     # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8' # Definindo a página de codificação de caracteres
MAX_LISTEN  = 10       # Definindo o máximo de conexões enfileiradas

mensagensLog = ['\n']
date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

caminhoServer = os.path.dirname(os.path.abspath(__file__))+'\\server_files'
caminhoLog = os.path.dirname(os.path.abspath(__file__))+'\\log_files'
def ajuda(CODE_PAGE,con):
        mensagem_volta = '\n --Listas de Comando-- \n \\f -- Listar Arquivos \n \\d:nome_arquivo -- Efetua o Download do Arquivo \n \\u:nome_arquivo -- Efetua o Upload do Arquivo \n \\q -- Sair do Cliente \n \\m -- listar Mensagens recebidas pelo servidor \n \\id -- listar id dos ususarios no sistema\n '                
        con.send(mensagem_volta.encode(CODE_PAGE))


def listArquivos(con,caminhoServer):
        listArquivos = os.listdir(caminhoServer)
        dictArquivos = {}
        for i in listArquivos:    
                dictArquivos.update({i:os.path.getsize(caminhoServer+'\\'+i)}) 
        arquivosTamanho =''
        for i,j in dictArquivos.items():
                arquivosTamanho = arquivosTamanho+i+';'+str(j)+'\n'
            
        if len(arquivosTamanho) > 0 :
                mensagem_volta = arquivosTamanho
                con.send(mensagem_volta.encode(CODE_PAGE))
        else:
                mensagem_volta = 'Sem Arquivos Disponíveis no Momento'
                con.send(mensagem_volta.encode(CODE_PAGE))

def mensagens(con,caminhoLog):        
        try:
                mensagenlog = '\n'
                with open(f'{caminhoLog}\\logServer.txt', 'r') as arquivo:             
                        linhas = arquivo.readlines()
                        for linha in linhas:
                                mensagenlog += f'{linha}'                        
                arquivo.close
                con.send(mensagenlog.encode(CODE_PAGE))                
        
        except:
                mensagem_volta = 'Arquivo log Inexistente'
                con.send(mensagem_volta.encode(CODE_PAGE))



def download(mensagem,con,caminhoServer):
        arquivo = mensagem.split(':',1)
        try:
                a = os.path.getsize(caminhoServer+'\\'+arquivo[1])
                mensagem_volta = str(a)
                con.send(mensagem_volta.encode(CODE_PAGE))             
    
                with open(caminhoServer+'\\'+arquivo[1],'rb') as arq:
                        for data in arq:                                   
                                con.send(data)
                                              
                arq.close()
        except:
                mensagem_volta = 'Arquivo Inesistente'
                con.send(mensagem_volta.encode(CODE_PAGE))                
              
                
       

def upload(caminhoServer,con,mensagem):
        try:
            arquivo = mensagem.split(':',1)


            with open(caminhoServer+'\\'+arquivo[1],'wb') as arq:                
                                                     
                while 1:                     
                    data_retorno = con.recv(BUFFER_SIZE)
                    arq.write(data_retorno)
                    sleep(0.0001) 
                    if len(data_retorno)<BUFFER_SIZE:break   

                                    

        except:
                mensagem_volta = f'\nERRO: {sys.exc_info()[0]}'
                con.send(mensagem_volta.encode(CODE_PAGE))                

def arquivoLog(mensagemLog):
        with open(f'{caminhoLog}\\logServer.txt', 'a') as arquivo:             
                arquivo.write(f'{mensagemLog}\n')
        arquivo.close

def youtube(pesquisa):
        YOUR_API_KEY = ''
        SEARCH = pesquisa
        TYPE = 'video'
        RESULT_NUM = '10'


        r = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?title&maxResults={RESULT_NUM}&q={SEARCH}%20&type={TYPE}&key={YOUR_API_KEY}')
        listVideo = r.json()
        lista = listVideo['items']
        listId = [] 
        videos = '\n'
        for i in lista:
        
                a = i['id']['videoId']
                listId.append(a) 
        for ID in listId:    
                p = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ID}&key={YOUR_API_KEY}')
                descri = p.json()    
        
                for i in descri['items']:           
                        canal = i['snippet']['channelTitle']
                        titulo = i['snippet']['title']
                        link = f'https://www.youtube.com/watch?v={ID}'
                        videos += (f'Canal: {canal}\nTítulo: {titulo}\nLink: {link}\n\n') 
        return videos

def twitter(usuario):
    try:
        
        TOKEN = ''
        headers = {
                    'Authorization': f'Bearer {TOKEN}',
                        'Content-Type': 'application/json',
                }


        r = requests.get(f'https://api.twitter.com/2/users/by/username/{usuario}?user.fields=name%2Cdescription%2Cpublic_metrics%2Cverified%2Clocation%2Curl',headers = headers )
        a = r.json()


        b = f" \n Nome: {a['data']['name']} \n Username: {a['data']['username']} \n Descrição: {a['data']['description']}\n Seguidores: {a['data']['public_metrics']['followers_count']} \n Seguindo: {a['data']['public_metrics']['following_count']}\n url: https://twitter.com/{a['data']['username']}"
        return b
    except:
        return('Usuario não existe')
def rss(pesquisa):
    url =['https://feeds.folha.uol.com.br/poder/rss091.xml','https://noticias.r7.com/feed.xml','https://feeds.elpais.com/mrss-s/pages/ep/site/brasil.elpais.com/portada']    

    TOKEN =  'ccf52e9d36f70b4489020d0f0e076283dd608108'

    
    materias_feed_lst = []
    noticias = '\n'
    for i in url:
        materias_feed_dic = feedparser.parse(i)
        materias_feed_lst += materias_feed_dic.entries
        
     
    for materias in materias_feed_lst: 
        portal = materias_feed_dic['feed']['title']    
        if pesquisa.upper() in materias.title.upper():  

            headers = {
                'Authorization': f'Bearer {TOKEN}',
                'Content-Type': 'application/json',
            }

            data = json.dumps({'long_url': materias.link , "domain": "bit.ly" })

            response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=data)
            links = response.json()
            links = links['link']
            noticias += f'\nPORTAL:{portal}\nTITULO: {materias.title} \nURL:{links}\n'
    
    return noticias