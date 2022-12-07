import socket, threading, sys
import sys
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
import csv


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






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Host")
        lab4 = QLabel("Port")

        self.__lab2 = QLabel("")
        self.__lab3 = QLabel("")
        self.__text = QLineEdit("")
        self.__text2 = QLineEdit("")
        ok = QPushButton("Ok")

        grid.addWidget(self.__lab3, 3, 1)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(lab, 0, 0)
        grid.addWidget(lab4, 1, 0)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 1, 1)

        grid.addWidget(ok, 5, 1)
        ok.clicked.connect(self.connexion)
        self.setWindowTitle("Application - Surveillance")




    def connexion(self):
        self.__lab2.setText(f"{self.__text.text()} | {self.__text2.text()}")
        # print(Client.msg)
        host = str(self.__text.text())
        port = int(self.__text2.text())
        client = Client(host, port)
        client.connect()
        client.dialogue()
        QCoreApplication.exit(0)
        # par exemple accès la socket




    def _actionQuitter(self):
        QCoreApplication.exit(0)






if __name__ == "__main__":
    # print(sys.argv)
    # if len(sys.argv) < 3:
    #     client = Client("127.0.0.1",15000)
    # else :
    #     host = sys.argv[1]
    #     port = int(sys.argv[2])
    #     # création de l'objet client qui est aussi un thread
    #     client = Client(host,port)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
