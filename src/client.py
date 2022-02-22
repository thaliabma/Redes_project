import socket
import threading
import time


# Para cores no terminal
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"
YELLOW = "\033[1;93m"
GREY = "\033[1;90m"


def main():

    # Criando o objeto cliente, com IPV4 e protocolo TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Endereço e a porta, que o cliente irá tentar se conectar
    try:
        client.connect(('localhost', 7777))
    except:
        return print(RED + '\n Não foi possível se conectar ao servidor\n' + RESET)

    # Usuário informa o nome
    print('\n\n ====== ' + BOLD + 'Olá! Seja bem-vindo(a) ao chat ' + RESET + CYAN + 'PAPO' + RESET +
          GREEN + 'EM' + RESET + CYAN + 'DIA' + RESET + '!' + YELLOW + ':) ' + RESET + '======')
    time.sleep(1)
    print(BOLD + '\nPor favor, digite o seu nome abaixo.' + RESET)
    usuario = input(BLUE + 'Usuário: ' + RESET)
    print(BOLD + '\nAguarde um momento e logo você estará no chat!' +
          RESET + YELLOW + ';)' + RESET)

    for i in range(0, 3):
        print(GREY + '.' + RESET)
        time.sleep(2)

    print(GREEN + '\nConectado.' + RESET)
    print('===============================')
    print(CYAN + '         PAPO' + GREEN+'EM' +
          RESET + CYAN + 'DIA           ' + RESET)
    print(BOLD + f'\n{usuario} ' + RESET + 'entrou no chat.')

    # Criando as threads recebe e envia
    thread_recebe = threading.Thread(target=Receber_mensagens, args=[client])
    thread_envia = threading.Thread(
        target=Enviar_mensagens, args=[client, usuario])

    # Inicializando as threads
    thread_recebe.start()
    thread_envia.start()


# Função responsável por receber mensagens de outros usuários
def Receber_mensagens(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print(RED + '\n Usuário está desconectado.\n' + RESET)
            print(GREEN + 'Pressione <Enter> para continuar.' + RESET)
            client.close()
            break

# Função responsável por enviar mensagens para os outros usuários


def Enviar_mensagens(client, usuario):
    primeira_vez = False
    while True:
        try:
            if(primeira_vez == False):
                msg = BOLD + usuario + RESET + ' entrou no chat.'
                client.send(f'{msg}'.encode('utf-8'))
                primeira_vez = True
            else:
                msg = input('\n')
                client.send(
                    f'\033[1;31m<{usuario}>\033[0;0m {msg}'.encode('utf-8'))
        except:
            return


main()
