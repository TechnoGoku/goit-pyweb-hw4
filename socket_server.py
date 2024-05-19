import socket


def main():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.listen()

    conn, address = server_socket.accept()
    print(f"Connected by: {address}")
    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            break
        print(f"Received by: {msg}")
        message = input(">>> ")
        conn.send(message.encode())
    conn.close()
    server_socket.close()


if __name__ == '__main__':
    main()
