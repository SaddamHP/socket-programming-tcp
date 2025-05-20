import socket
import threading

def receive_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                print("[!] Koneksi ke server terputus.")
                client.close()
                break
        except:
            print("[!] Error saat menerima pesan. Mungkin server terputus.")
            client.close()
            break

def send_messages(client, name):
    while True:
        try:
            message = input("")

            # Kirim sebagai private message jika formatnya @nama: pesan
            if message.startswith("@") and " " in message:
                client.send(message.encode('utf-8'))
            else:
                # Tambahkan nama pengirim ke pesan biasa
                full_message = message
                client.send(full_message.encode('utf-8'))
        except:
            print("[!] Gagal mengirim pesan.")
            client.close()
            break

# Membuat koneksi ke server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = input("Masukkan IP Server (contoh: localhost): ")

try:
    client.connect((server_ip, 2025))
except Exception as e:
    print(f"[!] Gagal terhubung ke server: {e}")
    exit()

# Input nama pengguna
name = input("Masukkan nama Anda: ")
client.send(name.encode('utf-8'))

print("\n📢 Selamat datang di Chat Room!")
print("Ketik pesan langsung untuk broadcast ke semua.")
print("Untuk kirim pesan pribadi, gunakan format: @nama_tujuan: pesan")
print("Contoh: @Andi: Halo Andi!\n")

# Mulai thread menerima dan mengirim pesan
threading.Thread(target=receive_messages, args=(client,)).start()
threading.Thread(target=send_messages, args=(client, name)).start()
