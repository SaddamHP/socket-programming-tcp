import socket
import threading

TCP_IP = 'localhost'
TCP_PORT = 2025

# Inisialisasi socket TCP IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen()

print(f"Server Chat Berjalan di {TCP_IP}:{TCP_PORT}...")

clients = []  # List koneksi client
names = {}     # Mapping client_socket -> nama pengguna

# Broadcast pesan ke semua client
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Tangani koneksi dari masing-masing client
def handle_client(client):
    name = client.recv(1024).decode('utf-8')  # Terima nama client
    names[client] = name
    welcome = f"{name} has joined the chat!"
    print(welcome)
    broadcast(welcome, sender_socket=client)

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                full_message = f"{name}: {message}"
                print(full_message)
                broadcast(full_message, sender_socket=client)
            else:
                break
        except:
            break

    # Client keluar
    print(f"{name} has left the chat.")
    broadcast(f"{name} has left the chat.")
    clients.remove(client)
    del names[client]
    client.close()

# Terima client baru
def receive_connections():
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
