import socket
import threading

# Function for receiving messages from the server


def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Error occured! Closing the client socket.")
            client_socket.close()
            break


def main():
    host = '127.0.0.1'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    nickname = input("Enter your nick: ")
    client_socket.send(nickname.encode('utf-8'))

    # Starting a new thread for receiving messages from the server
    receive_thread = threading.Thread(
        target=receive_message, args=(client_socket,))
    receive_thread.start()

    while True:
        option = input(
            "Write 'private' to start private conversation.\n Enter 'exit' to quit: ")
        if option.lower() == "exit":
            client_socket.send("exit".encode('utf-8'))
            break
        elif option.lower() == "private":
            recipient = input("Enter recipient's nickname: ")
            message = input("Enter message: ")
            client_socket.send(
                f"private message to: {recipient} {message}".encode('utf-8'))
        elif option.lower() == "show available groups":
            client_socket.send("Show available groups".encode('utf-8'))
        elif option.lower() == "join group":
            client_socket.send("Join group".encode('utf-8'))
        elif option.lower() == "create group":
            client_socket.send("Create group".encode('utf-8'))
        else:
            # Send the message to the server to broadcast
            client_socket.send(option.encode('utf-8'))
    client_socket.close()


if __name__ == "__main__":
    main()
