import socket
import threading
import os

client_socket = socket.socket()
client_socket.connect(('localhost', 10000))

def receive(client_socket):
    data = ""
    while data != "bye" and data != "arret":
        data = client_socket.recv(1024).decode()
        print(f"Message reçu du serveur : {data}")

t2 = threading.Thread(target=receive, args=[client_socket])
t2.start()
message = ""
while message != "bye" and message != "arret":
    message = input("Message à envoyer au Serveur : ")
    client_socket.send(message.encode())


t2.join()
client_socket.close()
