import socket,threading

HOST        = ''      # Definindo o IP do servidor
PORT        = 65000   # Definindo a porta
BUFFER_SIZE = 10      # Definindo o tamanho do buffer
CODE_PAGE   = 'utf-8' # Definindo a página de codificação de caracteres
MAX_LISTEN  = 10       # Definindo o máximo de conexões enfileiradas

# Criando o socket TCP
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcp_socket.bind((HOST, PORT)) # Ligando o socket a porta
tcp_socket.listen(MAX_LISTEN) # Máximo de conexões enfileiradas

print('Recebendo Mensagens...\n\n')
def ligar(BUFFER_SIZE,CODE_PAGE,tcp_socket):
    while True:
        con, cliente = tcp_socket.accept() # Aceita a conexão com o cliente
        print('Conectado por: ', cliente)
        while True:
            msg = con.recv(BUFFER_SIZE) #buffer de 1024 bytes
            if not msg: break
            # Imprimindo a mensagem recebida convertendo de bytes para string
            print(cliente, msg.decode(CODE_PAGE))
            # Devolvendo uma mensagem (echo) ao cliente
            msg_retorno = 'Devolvendo...' + msg.decode(CODE_PAGE)
            con.send(msg_retorno.encode(CODE_PAGE))
        

while True:
    cliente = threading.Thread(target=ligar, args=[BUFFER_SIZE,CODE_PAGE,tcp_socket])
    cliente.start()