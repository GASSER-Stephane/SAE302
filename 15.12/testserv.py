import socket
import subprocess
import platform
import psutil




def serveur():
    msg = ""
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()
        server_socket.bind(("0.0.0.0", 10007))
        server_socket.listen(10)

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
                        cmdping = msg.split(' ')
                        if cmd[0].lower() == "dos" and platform.platform()[:7] == "Windows":
                            # if cmd[1] == "dir":
                            try:
                                reply = subprocess.check_output(cmd[1], shell=True).decode('cp850').strip()
                            except:
                                reply = "[x] Commande Windows non reconnue. Vérifiez la syntaxe"
                                conn.send(reply.encode())
                            else:
                                if reply == "":
                                    reply = f"Commande {cmd[1]} effectuée"
                                    conn.send(reply.encode())
                                else:
                                    conn.send(reply.encode())
                        elif cmd[0].lower() == "powershell" and platform.platform()[:7] == "Windows":
                            try:
                                reply = subprocess.check_output(f"powershell.exe {cmd[1]}", shell=True).decode('cp850').strip()
                            except:
                                reply = "[x] Commande Powershell non reconnue. Vérifiez la syntaxe"
                                conn.send(reply.encode())
                            else:
                                conn.send(reply.encode())

                        elif msg.lower() == "Linux:ls -la":
                            reply = subprocess.check_output(msg.lower(), shell=True).decode('cp850').strip()
                            conn.send(reply.encode())

                        elif msg.lower() == "python --version":
                            reply = subprocess.check_output(msg.lower(), shell=True).decode('cp850').strip()
                            conn.send(reply.encode())

                        elif cmdping[0].lower() == "ping" and len(cmdping[1]) !=0:
                            reply = subprocess.check_output(f"ping {cmdping[1]}", shell=True).decode('cp850').strip()
                            conn.send(reply.encode())

                        elif msg.lower() == "os":
                            reply = platform.platform()
                            conn.send(reply.encode())

                        elif msg.lower() == "name":
                            reply = socket.gethostname()
                            conn.send(reply.encode())

                        elif msg.lower() == "ip":
                            hostname = socket.gethostname()
                            reply = socket.gethostbyname(hostname)
                            conn.send(reply.encode())

                        elif msg.lower() == "cpu":
                            reply = str(f"[+] Pourcentage du CPU utilisé : {psutil.cpu_percent()}%")
                            conn.send(reply.encode())

                        elif msg.lower() == "ram":
                            reply = str(
                                f"[+] Pourcentage de RAM utilisée : {psutil.virtual_memory().percent}%\n[+] RAM totale disponible {psutil.virtual_memory().total / 1024 / 1024} MB")
                            conn.send(reply.encode())

                        elif msg == "kill" or msg == "reset" or msg == "disconnect":
                            conn.send(msg.encode())
                        else:
                            reply = "[x] Aucune commande détectée. Veuillez ressayez !"
                            conn.send(reply.encode())
                except ConnectionResetError:
                    print("")
                except ConnectionAbortedError:
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