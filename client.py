import socket
import threading

# Menerima pesan dari server
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except:
            print("Connection lost.")
            sock.close()
            break

# Mengirim pesan ke server
def send_messages(sock):
    while True:
        try:
            message = input()
            if message:
                sock.send(message.encode('utf-8'))
        except:
            break

# Buat koneksi ke server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = input("Enter server IP (e.g., localhost): ")
client.connect((server_ip, 12345))

# Input nama pengguna
name = input("Enter your name: ")
client.send(name.encode('utf-8'))

# Mulai thread menerima dan mengirim pesan
threading.Thread(target=receive_messages, args=(client,)).start()
threading.Thread(target=send_messages, args=(client,)).start()
