import socket
import threading
import sys

SERVER_PORT = 8000
SERVER_IP = ''
clients = []


def bind_to_the_server():
    tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_server = (SERVER_IP, SERVER_PORT)
    tcp_connection.bind(socket_server)
    tcp_connection.listen(5)  # Permitir até 5 conexões

    return tcp_connection


def client_handler(connection, ip_client, username):
    broadcast(f"{username} entrou no chat.")
    while True:
        rec_message = connection.recv(1024).decode()
        if not rec_message or rec_message == 'exit':
            broadcast(f"{username} saiu do chat.")
            break
        print(f"\n{username} ({ip_client}): {rec_message}")
        broadcast(f"{username}: {rec_message}", connection)


def broadcast(message, sender_connection=None):
    for client in clients:
        if client != sender_connection:
            try:
                client.send(message.encode())
            except:
                client.close()
                remove(client)


def remove(connection):
    if connection in clients:
        clients.remove(connection)


def accepting_connections(tcp_connection):
    while True:
        connection, ip_client = tcp_connection.accept()
        username = connection.recv(1024).decode()
        print(f"\n{username} está conectado.")
        clients.append(connection)
        client_thread = threading.Thread(target=client_handler, args=(connection, ip_client[0], username))
        client_thread.start()


if __name__ == '__main__':
    host_name = socket.gethostname()
    s_ip = socket.gethostbyname(host_name)

    print("Servidor ligado com sucesso...")
    print("Esse é seu IP:", s_ip)

    current_connection = bind_to_the_server()
    accepting_connections(current_connection)

    sys.exit()
