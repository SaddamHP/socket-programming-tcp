import socket
import threading
import sys

def coba_koneksi(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try :
        client_socket.connect((ip, port))
        return client_socket
    except :
        return None

# Menerima pesan dari server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
                print(f"[Kirim Sebagai ({name})]> ", end="", flush=True)
            else:
                break
        except:
            print("Koneksi Terputus.")
            sock.close()
            break

# Mengirim pesan ke server
def send_messages(sock):
    while True:
        try:
            message = input(f"[Kirim Sebagai ({name})]> ")
            if message:
                sock.send(message.encode('utf-8'))
        except:
            break

# Buat koneksi ke server
server_ip = input("Masuk ke Server IP (localhost): ")
server_port = 2025

client = coba_koneksi(server_ip, server_port)

if client is None:
    print(f"Tidak dapat terhubung ke {server_ip}:{server_port}")
    sys.exit()
else:
    print(f"Terhubung ke {server_ip}:{server_port}")

# Input nama pengguna
name = input("Enter your name: ")
client.send(name.encode('utf-8'))

# Mulai thread menerima dan mengirim pesan
threading.Thread(target=receive_messages, args=(client,)).start()
threading.Thread(target=send_messages, args=(client,)).start()