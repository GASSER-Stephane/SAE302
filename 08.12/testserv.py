import socket
import threading
import os
import subprocess
import platform
import psutil




def serveur():
    msg = ""
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 15000))
        server_socket.listen(1)

        print('Serveur en attente de connexion')
        while msg != "kill" and msg != "reset":
            msg = ""
            try :
                conn, addr = server_socket.accept()
                print (addr)
            except ConnectionError:
                print ("Erreur de connection")
                break
            else :
                try:
                    while msg != "kill" and msg != "reset" and msg != "disconnect":
                        msg = conn.recv(1024).decode()
                        print ("Reçu du client : ", msg)
                        cmd = msg.split(':')
                        if cmd[0] == "DOS" and platform.platform()[:7] == "Windows":
                            if cmd[1] == "dir":
                                reply = subprocess.getoutput("dir")
                                conn.send(reply.encode())
                                print(f"Checkbug : DIR FAIT")
                            elif cmd[1][:6] == "mkdir ":
                                if len(cmd[1][6:]) != 0:
                                    dos = cmd[1][6:]
                                    reply = subprocess.getoutput(f"mkdir U:\Documents\BUT2\SAE3.02\SAE3.02\{dos}")[228:]
                                    conn.send(reply.encode())
                                    print(f"Checkbug : MKDIR {dos} FAIT")
                                else:
                                    print("Impossible de créer un dossier sans nom")
                            else:
                                print("Erreur : Commande Windows incomplète ou inconnue")
                        elif cmd[0] == "Powershell" and platform.platform()[:7] == "Windows":
                            if cmd[1] == "get-process":
                                reply = subprocess.getoutput("powershell.exe get-process")
                                conn.send(reply.encode())
                                print(f"Checkbug : Powershell:get-process FAIT")
                            else:
                                print("Erreur : Commande Powershell inconnue")
                        elif msg == "Linux:ls -la":
                            reply = subprocess.getoutput("ls -la")
                            conn.send(reply.encode())
                            print(f"Checkbug : ls -la FAIT")
                        elif msg == "python --version":
                            reply = subprocess.getoutput("python --version")[228:]
                            conn.send(reply.encode())
                            print(f"Checkbug : python --version FAIT")
                        elif msg == "ping 192.168.152.1":
                            reply = subprocess.getoutput("ping 192.168.152.1")
                            conn.send(reply.encode())
                            print(f"Checkbug : PING FAIT")
                        elif msg == "OS":
                            reply = platform.platform()
                            conn.send(reply.encode())
                            print("OS renvoyé")
                        elif msg == "Name":
                            reply = socket.gethostname()
                            conn.send(reply.encode())
                            print("Nom envoyé")
                        elif msg == "IP":
                            hostname = socket.gethostname()
                            reply = socket.gethostbyname(hostname)
                            conn.send(reply.encode())
                            print("IP envoyé")
                        elif msg == "CPU":
                            reply = str(f"{psutil.cpu_percent()}% du CPU utilisé !")
                            conn.send(reply.encode())
                            print("Checkbug : Info CPU envoyée")
                        elif msg == "RAM":
                            reply = str(
                                f"{psutil.virtual_memory().percent}% de la RAM utilisé ! \nRAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
                            conn.send(reply.encode())
                            print("Checkbug : Info RAM envoyée")
                        elif msg == "kill" or msg == "reset" or msg == "disconnect":
                            conn.send(msg.encode())
                        # else:
                        #     reply = "T CON"
                        #     conn.send(reply.encode())
                except ConnectionResetError:
                    print("")
                except KeyboardInterrupt:
                    print("Application arrêtée brusquement")
                conn.close()
        print ("Connexion fermée")
        server_socket.close()
        print ("Serveur fermé")

# Coder les commande ici

if __name__ == '__main__':
    serveur()