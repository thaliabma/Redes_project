import threading  # intuito de usar multiThreads
import socket
from datetime import datetime
# cria uma lista, poistodo cliente que chega é armazenado em uma lista.
clients = []
total = 0
m = []
cont = 0
# cria a função principal

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
YELLOW = "\033[1;93m"
GREY = "\033[1;90m"


def main():
    global cont
    global total
    data_atuais = datetime.now()
    data_texto = data_atuais.strftime('%d/%m/%Y %H:%M')

    # cria o objeto socket passando os parâmetros: família de endereços e o tipo de socket(TCP)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # tentar fazer a ligação do servidor
    try:
        server.bind(('localhost', 7777))
        server.listen()  # servidor vai estar pronto para se conectar
        print(BLUE + f'\nChat Aberto em {data_texto}' + RESET)
        print(RED + "Esperando conexão de clientes..." + RED + RESET)
    except:
        # caso não consiga ligar o servidor
        return print(RED + '\nNão foi possível iniciar o servidor!\n' + RESET)

    # aceita as conecções
    while True:
        client, addr = server.accept()  # essas conecções retornam dois endereços
        clients.append(client)  # adiciona o cliente na "lista dos clientes"
        total = total + 1
        print('\nNovo usuário foi' + GREEN + ' CONECTADO. ' +
              RESET + f'Total de {total} membro(s)!')

        if cont != 0:
            client.send(bytes('\n', encoding="utf-8"))
            for i in range(cont):
                client.send(m[i])
                client.send(bytes('\n\n', encoding="utf-8"))

        # iniciar uma thread para cada novo cliente
        thread = threading.Thread(target=messagesTreatment, args=[client])
        thread.start()


def messagesTreatment(client):  # escuta as mensagens dos clientes
    global cont
    primeiro = False
    while True:
        try:
            if(primeiro == False):
                nome = client.recv(2048)
                broadcast(nome, client)
                primeiro = True
            else:
                msg = client.recv(2048)
                cont = cont + 1
                m.append(msg)
            # mensagem é enviada para todos os outros clientes menos para quem a enviou
                broadcast(msg, client)
        except:
            # caso não seja possível receber a mensagem do cliente, ele foi desconectado, deletar ele da lista
            deleteClient(client)
            break  # parar de ouvir mensagem desse cliente, já que ele não esta mais conectado


def broadcast(msg, client):
    for clientItem in clients:  # percorre cada um dos clientes para ver quais vão receber a mensagem nova
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                # caso nao consiga mandar a mensagem, é porque o cliente foi desconectado, deve-se tirar ele da lista
                deleteClient(clientItem)


def deleteClient(client):
    global total
    global cont
    total = total - 1
    if total == 0:
        print('\nUm usuário foi' + RED + ' DESCONECTADO. ' +
              RESET + f'Total de {total} membro(s)!')
        print(BOLD + '\nChat Vazio. Sem membros no momento...' + RESET)
        m.clear()
        cont = 0
    else:
        print('\nUm usuário foi' + RED + ' DESCONECTADO. ' +
              RESET + f'Total de {total} membro(s)!')

    clients.remove(client)


# executa a função principal novamente
main()
