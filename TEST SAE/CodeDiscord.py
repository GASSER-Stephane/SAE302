import socket, threading, sys


class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None

    # fonction de connection.
    def connect(self) -> int:
        try :
            self.__sock.connect((self.__host,self.__port))
        except ConnectionRefusedError:
            print ("[X] Serveur non lancé ou mauvaise information")
            return -1
        except ConnectionError:
            print ("[X] Erreur de connection")
            return -1
        else :
            print ("[+] Connexion réalisée")
            return 0


    def dialogue(self):
        msg = ""
        self.__thread = threading.Thread(target=self.__reception, args=[self.__sock,])
        self.__thread.start()
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.__envoi()
        self.__thread.join()
        self.__sock.close()

    # méthode d'envoi d'un message au travers la socket. Le résultat de cette methode est le message envoyé.
    def __envoi(self):
        msg = input("Message à envoyer au Serveur : ")
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            print ("erreur, socket fermée")
        return msg
    """
      thread recepction, la connection étant passée en argument
    """
    def __reception(self, conn):
        msg =""
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = conn.recv(1024).decode('cp850')
            print(msg)



if __name__ == "__main__":

    print(sys.argv)
    if len(sys.argv) < 3:
        client = Client("127.0.0.1",15001)
    else :
        host = sys.argv[1]
        port = int(sys.argv[2])
        # création de l'objet client qui est aussi un thread
        client = Client(host,port)
    client.connect()
    client.dialogue()