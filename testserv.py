import socket
import threading
import os
import subprocess
import platform
import psutil

server_socket = socket.socket()
server_socket.bind(('localhost', 10000))
reply = ""
data = ""
server_socket.listen(1)
conn, address = server_socket.accept()


def commande(data):
    cmd = data.split(':')
    if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
        if cmd[1] == "dir":
            reply = subprocess.getoutput("dir")[228:]
            conn.send(reply.encode())
            print(f"Checkbug : DIR FAIT")
        elif cmd[1][:6] == "mkdir ":
            if len(cmd[1][6:]) != 0:
                dos =cmd[1][6:]
                reply = subprocess.getoutput(f"mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\{dos}")[228:]
                conn.send(reply.encode())
                print(f"Checkbug : MKDIR {dos} FAIT")
            else:
                print("Impossible de créer un dossier sans nom")
        else:
            print("Erreur : Commande Windows incomplète ou inconnue")
    elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
        if cmd[1] == "get-process":
            reply = subprocess.getoutput("powershell.exe get-process")[228:]
            conn.send(reply.encode())
            print(f"Checkbug : Powershell:get-process FAIT")
        else:
            print("Erreur : Commande Powershell inconnue")
    elif data == "Linux:ls -la":
        reply = subprocess.getoutput("ls -la")
        conn.send(reply.encode())
        print(f"Checkbug : ls -la FAIT")
    elif data == "python --version":
        reply = subprocess.getoutput("python --version")[228:]
        conn.send(reply.encode())
        print(f"Checkbug : python --version FAIT")
    elif data == "ping 192.168.152.1":
        reply = subprocess.getoutput("ping 192.168.152.1")[228:]
        conn.send(reply.encode())
        print(f"Checkbug : PING FAIT")
    elif data == "OS":
        reply = platform.platform()
        conn.send(reply.encode())
        print("OS renvoyé")
    elif data == "Name":
        reply = socket.gethostname()
        conn.send(reply.encode())
        print("Nom envoyé")
    elif data == "IP":
        hostname = socket.gethostname()
        reply = socket.gethostbyname(hostname)
        conn.send(reply.encode())
        print("IP envoyé")
    elif data == "CPU":
        reply = str(f"{psutil.cpu_percent()}% du CPU utilisé !")
        conn.send(reply.encode())
        print("Checkbug : Info CPU envoyée")
    elif data == "RAM":
        reply = str(f"{psutil.virtual_memory().percent}% de la RAM utilisé ! \nRAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
        conn.send(reply.encode())
        print("Checkbug : Info RAM envoyée")
    else:
        print(f"Message reçu du client : {data}")





def recept(conn):
    data=""
    while data != "bye":
        data = conn.recv(1024).decode()
        commande(data)









t2 = threading.Thread(target=recept, args=[conn])
t2.start()

while reply != "arret" and data != "arret":
        reply = ""
        data = ""
        while reply != "bye" and data != "bye":
            reply=input("Message à envoyer au Client : ")
            conn.send(reply.encode())
        conn.close()
server_socket.close()




#On doit boucler le conn.accept puis conn.close qui ferme la connexion avec le client (msg bye)
#On serveur_socket.close pour fermer le server (msg arret)










































# #------------------------------- FONCTIONNE --------------------------
# import socket
# import threading
# import os
# import subprocess
# import platform
# import psutil
#
# server_socket = socket.socket()
# server_socket.bind(('localhost', 10000))
# reply = ""
# data = ""
# server_socket.listen(1)
# conn, address = server_socket.accept()
#
#
# def commande(data):
#     cmd = data.split(':')
#     if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "dir":
#             reply = subprocess.getoutput("dir")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : DIR FAIT")
#         elif cmd[1] == "mkdir toto":
#             reply = subprocess.getoutput("mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\Toto")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : MKDIR TOTO FAIT")
#         else:
#             print("Erreur : Commande Windows inconnue")
#     elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "get-process":
#             reply = subprocess.getoutput("powershell.exe get-process")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : Powershell:get-process FAIT")
#         else:
#             print("Erreur : Commande Powershell inconnue")
#
#
#     elif data == "Linux:ls -la":
#         reply = subprocess.getoutput("ls -la")
#         conn.send(reply.encode())
#         print(f"Checkbug : ls -la FAIT")
#     elif data == "python --version":
#         reply = subprocess.getoutput("python --version")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : python --version FAIT")
#     elif data == "ping 192.168.152.1":
#         reply = subprocess.getoutput("ping 192.168.152.1")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : PING FAIT")
#     elif data == "OS":
#         reply = platform.platform()
#         conn.send(reply.encode())
#         print("OS renvoyé")
#     elif data == "Name":
#         reply = socket.gethostname()
#         conn.send(reply.encode())
#         print("Nom envoyé")
#     elif data == "IP":
#         hostname = socket.gethostname()
#         reply = socket.gethostbyname(hostname)
#         conn.send(reply.encode())
#         print("IP envoyé")
#
#
#
#
#     elif data == "CPU":
#         reply = psutil.cpu_percent()
#         conn.send(reply.encode())
#         print("Info CPU envoyée")
#     elif data == "RAM":
#         reply = psutil.virtual_memory().percent
#         conn.send(reply.encode())
#         print("Info RAM envoyée")
#     else:
#         print(f"Message reçu du client : {data}")
#
#
#
#
#
# def recept(conn):
#     data=""
#     print(f"RAM total is {psutil.virtual_memory().total / 1024 / 1024}")
#     print(f"Mémoire disponible : {psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}")
#     print(f"Pourcentage RAM utilisé: {psutil.virtual_memory().percent}%")
#
#     while data != "bye":
#         data = conn.recv(1024).decode()
#         commande(data)
#
#
#
#
#
#
#
#
#
# t2 = threading.Thread(target=recept, args=[conn])
# t2.start()
#
# while reply != "arret" and data != "arret":
#         reply = ""
#         data = ""
#         while reply != "bye" and data != "bye":
#             reply=input("Message à envoyer au Client : ")
#             conn.send(reply.encode())
#         conn.close()
# server_socket.close()
#
#
#
#
# #On doit boucler le conn.accept puis conn.close qui ferme la connexion avec le client (msg bye)
# #On serveur_socket.close pour fermer le server (msg arret)



# import socket
# import threading
# import os
# import subprocess
# import platform
# import psutil
#
# server_socket = socket.socket()
# server_socket.bind(('localhost', 10000))
# reply = ""
# data = ""
# server_socket.listen(1)
# conn, address = server_socket.accept()
#
#
# def commande(data):
#     cmd = data.split(':')
#     test = ""
#     if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "dir":
#             reply = subprocess.getoutput("dir")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : DIR FAIT")
#         elif cmd[1][:6] == f"mkdir ":
#             test = cmd[1][6:]
#             reply = subprocess.getoutput(f"mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\{test}")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : Dossier {test} FAIT")
#         else:
#             print("Erreur : Commande Windows inconnue")
#     elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "get-process":
#             reply = subprocess.getoutput("powershell.exe get-process")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : Powershell:get-process FAIT")
#         else:
#             print("Erreur : Commande Powershell inconnue")
#
#
#     elif data == "Linux:ls -la":
#         reply = subprocess.getoutput("ls -la")
#         conn.send(reply.encode())
#         print(f"Checkbug : ls -la FAIT")
#     elif data == "python --version":
#         reply = subprocess.getoutput("python --version")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : python --version FAIT")
#     elif data == "ping 192.168.152.1":
#         reply = subprocess.getoutput("ping 192.168.152.1")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : PING FAIT")
#     elif data == "OS":
#         reply = platform.platform()
#         conn.send(reply.encode())
#         print("Checkbug : OS renvoyé")
#     elif data == "Name":
#         reply = socket.gethostname()
#         conn.send(reply.encode())
#         print("Checkbug : Nom envoyé")
#     elif data == "IP":
#         hostname = socket.gethostname()
#         reply = socket.gethostbyname(hostname)
#         conn.send(reply.encode())
#         print("Checkbug : IP envoyée")
#
#     elif data == "CPU":
#         reply = str(f"{psutil.cpu_percent()}% du CPU utilisé !")
#         conn.send(reply.encode())
#         print("Checkbug : Info CPU envoyée")
#     elif data == "RAM":
#         reply = str(f"{psutil.virtual_memory().percent}% de la RAM utilisé ! \nRAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
#         conn.send(reply.encode())
#         print("Checkbug : Info RAM envoyée")
#     else:
#         print(f"Message reçu du client : {data}")
#
#
#
#
#
# def recept(conn):
#     data=""
#     while data != "bye":
#         data = conn.recv(1024).decode()
#         commande(data)
#     else:
#         conn.close()
#
#
#
#
# t2 = threading.Thread(target=recept, args=[conn])
# t2.start()
#
# while reply != "reset" and data != "reset":
#     conn, address = server_socket.accept()
#     reply = ""
#     data = ""
#     while reply != "bye" and data != "bye":
#             reply=input("Message à envoyer au Client : ")
#             data = conn.recv(1024).decode()
#             conn.send(reply.encode())
#             print(f"Message reçu du client {data}")
#     conn.close()
# server_socket.close()
#
# t2.join()
#
#
# #On doit boucler le conn.accept puis conn.close qui ferme la connexion avec le client (msg bye)
#
#
#
# #On serveur_socket.close pour fermer le server (msg arret)







































# #------------------------------- FONCTIONNE --------------------------
# import socket
# import threading
# import os
# import subprocess
# import platform
# import psutil
#
# server_socket = socket.socket()
# server_socket.bind(('localhost', 10000))
# reply = ""
# data = ""
# server_socket.listen(1)
# conn, address = server_socket.accept()
#
#
# def commande(data):
#     cmd = data.split(':')
#     if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "dir":
#             reply = subprocess.getoutput("dir")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : DIR FAIT")
#         elif cmd[1] == "mkdir toto":
#             reply = subprocess.getoutput("mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\Toto")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : MKDIR TOTO FAIT")
#         else:
#             print("Erreur : Commande Windows inconnue")
#     elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
#         if cmd[1] == "get-process":
#             reply = subprocess.getoutput("powershell.exe get-process")[228:]
#             conn.send(reply.encode())
#             print(f"Checkbug : Powershell:get-process FAIT")
#         else:
#             print("Erreur : Commande Powershell inconnue")
#
#
#     elif data == "Linux:ls -la":
#         reply = subprocess.getoutput("ls -la")
#         conn.send(reply.encode())
#         print(f"Checkbug : ls -la FAIT")
#     elif data == "python --version":
#         reply = subprocess.getoutput("python --version")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : python --version FAIT")
#     elif data == "ping 192.168.152.1":
#         reply = subprocess.getoutput("ping 192.168.152.1")[228:]
#         conn.send(reply.encode())
#         print(f"Checkbug : PING FAIT")
#     elif data == "OS":
#         reply = platform.platform()
#         conn.send(reply.encode())
#         print("OS renvoyé")
#     elif data == "Name":
#         reply = socket.gethostname()
#         conn.send(reply.encode())
#         print("Nom envoyé")
#     elif data == "IP":
#         hostname = socket.gethostname()
#         reply = socket.gethostbyname(hostname)
#         conn.send(reply.encode())
#         print("IP envoyé")
#
#
#
#
#     elif data == "CPU":
#         reply = psutil.cpu_percent()
#         conn.send(reply.encode())
#         print("Info CPU envoyée")
#     elif data == "RAM":
#         reply = psutil.virtual_memory().percent
#         conn.send(reply.encode())
#         print("Info RAM envoyée")
#     else:
#         print(f"Message reçu du client : {data}")
#
#
#
#
#
# def recept(conn):
#     data=""
#     print(f"RAM total is {psutil.virtual_memory().total / 1024 / 1024}")
#     print(f"Mémoire disponible : {psutil.virtual_memory().available * 100 / psutil.virtual_memory().total}")
#     print(f"Pourcentage RAM utilisé: {psutil.virtual_memory().percent}%")
#
#     while data != "bye":
#         data = conn.recv(1024).decode()
#         commande(data)
#
#
#
#
#
#
#
#
#
# t2 = threading.Thread(target=recept, args=[conn])
# t2.start()
#
# while reply != "arret" and data != "arret":
#         reply = ""
#         data = ""
#         while reply != "bye" and data != "bye":
#             reply=input("Message à envoyer au Client : ")
#             conn.send(reply.encode())
#         conn.close()
# server_socket.close()
#
#
#
#
# #On doit boucler le conn.accept puis conn.close qui ferme la connexion avec le client (msg bye)
# #On serveur_socket.close pour fermer le server (msg arret)
