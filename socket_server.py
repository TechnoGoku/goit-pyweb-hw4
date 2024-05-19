import socket


def main():
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    server_socket.listen()

    conn, address = server_socket.accept()
    print(f"Connected by: {address}")

if __name__ == '__main__':
    main()