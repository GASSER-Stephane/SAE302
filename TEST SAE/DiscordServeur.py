import socket
import subprocess

def serveur():
    msg = ""
    conn = None
    server_socket = None
    while msg != "kill" :
        msg = ""
        server_socket = socket.socket()

# l'adresse 0.0.0.0 permet d'écouter toutes les IP de la machine, localhost, locale comme publique
        server_socket.bind(("0.0.0.0", 15001))

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
                while msg != "kill" and msg != "reset" and msg != "disconnect":
                    msg = conn.recv(1024).decode()
                    print ("Reçu du client : ", msg)
                    if msg == "dir":
                        reply = subprocess.getoutput("dir")
                        conn.send(reply.encode())
                    elif msg == "kill" or msg == "reset" or msg == "disconnect":
                        conn.send(msg.encode())
                conn.close()
        print ("Connexion fermée")
        server_socket.close()
        print ("Serveur fermé")

# Coder les commande ici

if __name__ == '__main__':
    serveur()