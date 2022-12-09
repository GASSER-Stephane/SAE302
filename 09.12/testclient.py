import socket, threading, sys
import sys
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
import csv
from testserv import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None
        # self.__msg = msg #//



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

    def connexion(self):
        self.__sock.connect((self.__host, self.__port))



    def dialogue(self, msg):
        # self.__thread = threading.Thread(target=self.reception, args=[msg])
        # self.__thread.start()
        # while msg != "kill" and msg != "disconnect" and msg != "reset":
        #      msg = self.envoi()
        # self.__thread.join()
        # self.__sock.close()
        try:
                msg = self.__sock.recv(1024).decode('cp850')
                return msg
        except:
            print("Y a un soucis")

    def reception(self, msg):
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.__sock.recv(1024).decode('cp850')
            return msg

    # méthode d'envoi d'un message au travers la socket. Le résultat de cette methode est le message envoyé.
    def envoi(self, msg):
        # msg = input("Message à envoyer au Serveur : ")
        self.__sock.send(msg.encode())
        reponse = self.__sock.recv(32000).decode()
        return reponse
    """
      thread recepction, la connection étant passée en argument
    """












class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Host")
        lab4 = QLabel("Port")
        lab3 = QLabel("Votre commande : ")
        self.__lab2 = QLabel("")
        self.__lab3 = QTextEdit(self)
        self.__lab4 = QLabel("")
        self.__text = QLineEdit("")
        self.__text2 = QLineEdit("")
        self.__text3 = QLineEdit("")
        self.__client = None
        okcon = QPushButton("Connexion")
        okcom = QPushButton("Envoyer")
        # okcomcom = QPushButton("Envoyer Envoyer")


        grid.addWidget(self.__lab3, 3, 1)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(self.__lab4, 1, 1)
        grid.addWidget(lab, 0, 0)
        grid.addWidget(lab4, 1, 0)
        grid.addWidget(lab3, 2, 0)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__text2, 1, 1)
        grid.addWidget(self.__text3, 2, 1)
        self.__text.setText("127.0.0.1")
        self.__text2.setText("15000")
        self.__text3.setText("python --version")

        grid.addWidget(okcon, 5, 1)
        grid.addWidget(okcom, 2, 2)
        # grid.addWidget(okcomcom, 6, 2)
        okcon.clicked.connect(self.okconnexion)
        okcom.clicked.connect(self.okcommande)
        # okcomcom.clicked.connect(self.okokcommande)
        self.setWindowTitle("Application - Surveillance")

    def okcommande(self):
        msg = self.__text3.text()
        reponse = self.__client.envoi(msg)
        # self.__lab3.setText(f"Commande  : {msg}\n")
        self.__lab3.setText(f"{reponse}")

    #
    # def okokcommande(self):
    #     msg = self.__text3.text()
    #     self.__client.dialogue(msg)
    #     self.__lab2.setText(f"Réponse : {self.__client.dialogue(msg)}")

    def okconnexion(self):
        # self.__lab2.setText(f"Host / Port : {self.__text.text()} | {self.__text2.text()}")
        host = str(self.__text.text())
        port = int(self.__text2.text())
        self.__client = Client(host, port)
        self.__client.connexion()

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
    # client.connect()
    # client.dialogue()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
