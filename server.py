import socket
import threading

TCP_IP = 'localhost'
TCP_PORT = 2025

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen()

print(f"Server Chat Berjalan di {TCP_IP}:{TCP_PORT}...")

clients = []            # List koneksi client
names = {}              # client_socket -> nama
sockets_by_name = {}    # nama -> client_socket

# Kirim pesan ke semua client kecuali pengirim
def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Kirim pesan pribadi
def private_message(sender_name, target_name, message):
    target_socket = sockets_by_name.get(target_name)
    if target_socket:
        try:
            msg = f"[Private] {sender_name} ➤ {target_name}: {message}"
            target_socket.send(msg.encode('utf-8'))
        except:
            target_socket.close()
            clients.remove(target_socket)
    else:
        # Jika target tidak ditemukan
        sender_socket = sockets_by_name.get(sender_name)
        if sender_socket:
            sender_socket.send(f"[Server] Pengguna '{target_name}' tidak ditemukan.".encode('utf-8'))

# Tangani koneksi dan pesan client
def handle_client(client):
    name = client.recv(1024).decode('utf-8')
    names[client] = name
    sockets_by_name[name] = client
    welcome = f"{name} has joined the chat!"
    print(welcome)
    broadcast(welcome, sender_socket=client)

    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                # Cek apakah pesan private
                if message.startswith("@"):
                    # Format: @nama_tujuan: pesan
                    if ':' in message:
                        target_and_msg = message[1:].split(':', 1)
                        target_name = target_and_msg[0].strip()
                        private_msg = target_and_msg[1].strip()
                        private_message(name, target_name, private_msg)
                    else:
                        client.send("[Server] Format pesan privat salah. Gunakan @nama: pesan".encode('utf-8'))
                else:
                    # Broadcast ke semua
                    full_message = f"{name}: {message}"
                    print(full_message)
                    broadcast(full_message, sender_socket=client)
            else:
                break
        except:
            break

    # Saat client keluar
    print(f"{name} has left the chat.")
    broadcast(f"{name} has left the chat.")
    clients.remove(client)
    del names[client]
    del sockets_by_name[name]
    client.close()

# Menerima koneksi client baru
def receive_connections():
    while True:
        client, addr = server.accept()
        print(f"Connected with {addr}")
        clients.append(client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive_connections()
