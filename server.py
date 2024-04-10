import socket
import threading

# Function for broadcasting messages to all clients


def broadcast(message, nickname, clients):
    for client_socket in clients:
        client_socket.send(f"{nickname}: {message}".encode('utf-8'))


def handle_client(client_socket, clients):
    nickname = client_socket.recv(1024).decode('utf-8')
    clients.append((client_socket, nickname))
    broadcast(f"Bienvenue cher/chère {nickname}!".encode('utf-8'))

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('private message to:'):
                recipient, message = message.split(' ', 2)[3:]
                for client, nickname in clients:
                    if nickname == recipient:
                        client.send(
                            f"Private message from {nickname}: {message}".encode('utf-8'))
                        break
                else:
                    client_socket.send(
                        f"Recipient '{recipient}' not found.".encode('utf-8'))
            elif message.startswith('Join group'):
                channel = message.split(' ', 2)[2]
                client_socket.send(
                    f"Joined channel {channel}".encode('utf-8'))
            elif message.startswith('Create group'):
                group_name = message.split(': ')[1]
                broadcast(
                    f"{nickname} created channel {group_name}".encode('utf-8'))

            elif message == "exit":
                print(f"Au revoir, à la prochaine {nickname}!")
                client_socket.close()
                clients.remove(client_socket)
                break
            else:
                broadcast(message, nickname, clients)
        except:
            print(f"Au revoir, à la prochaine {nickname}!")
            client_socket.close()
            clients.remove(client_socket)
            break

# Function for sending private messages to a specific client


def send_private_message(clients):
    while True:
        recipient = input("Enter recipient's nickname: ")
        message = input("Enter message: ")
        for client, nickname in clients.items():
            if nickname == recipient:
                client.send(
                    f"Private message from {nickname}: {message}".encode('utf-8'))
                break
        else:
            print(f"Recipient '{recipient}' not found.")


def broadcast_to_channel(message, channel, sender_nickname, clients):
    for client_socket, nickname in clients:
        if nickname != sender_nickname and nickname == channel:
            client_socket.send(
                f"{sender_nickname} (channel {channel}): {message}".encode('utf-8'))


def main():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    clients = []

    print(f"Server is running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
        clients.append(client_socket)

        # Starting a new thread for each client
        client_thread = threading.Thread(
            target=handle_client, args=(client_socket, clients))
        client_thread.start()


if __name__ == "__main__":
    main()
