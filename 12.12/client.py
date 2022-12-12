import socket, threading, sys
import sys
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QCoreApplication
import csv
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
        self.__labtitre = QLabel("Bienvenue sur Surveil'App !\n Veuillez vous connectez")
        self.__lab = QLabel("Host")
        self.__lab8 = QLabel("Port")
        self.__labadd = QLabel("Nouvelle Co.")
        self.__btnadd = QPushButton("Ajouter")
        self.__labtitre.setFont(QFont('Arial', 25))
        self.__lab5 = QLabel("Votre commande : ")
        self.__lab9 = QLabel("Résultat : ")
        self.__info = QLabel("Informations \n( Host / Port )")
        self.__lab2 = QLabel("")
        self.__text10 = QLineEdit("")
        self.__lab3 = QTextEdit(self)
        self.__labtitre.setAlignment(Qt.AlignCenter)
        self.__lab4 = QLabel("")
        self.__text = QComboBox()
        self.__text2 = QLineEdit("")
        self.__text3 = QLineEdit("")
        self.__infohost = QLineEdit("")
        self.__infoport = QLineEdit("")
        self.__infoportlabel = QLabel("")
        self.__infohostlabel = QLabel("")



        self.__client = None
        self.__okcon = QPushButton("Connexion")
        self.__okcom = QPushButton("Envoyer")
        self.__deco = QPushButton("Déconnexion")
        self.__nouvelco = QPushButton("Nouvelle Co.")

        # Using readlines()
        file1 = open('OMG.txt.txt', 'r')
        Lines = file1.readlines()

        count = 0
        # Strips the newline character
        for line in Lines:
            count += 1
            self.__text.addItem(line.strip())
        self.__lab3.hide()
        self.__lab5.hide()
        self.__text3.hide()
        grid.addWidget(self.__labtitre, 0, 1)
        grid.addWidget(self.__info, 0, 0)
        grid.addWidget(self.__labadd, 5, 0)
        grid.addWidget(self.__btnadd, 5, 2)

        grid.addWidget(self.__infohost, 0, 1)
        grid.addWidget(self.__infoport, 0, 2)
        grid.addWidget(self.__infoportlabel, 0, 2)
        grid.addWidget(self.__infohostlabel, 0, 1)
        grid.addWidget(self.__lab3, 3, 1, 1, 5)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(self.__lab4, 1, 1)
        grid.addWidget(self.__lab, 2, 0)
        grid.addWidget(self.__lab8, 3, 0)
        grid.addWidget(self.__lab5, 2, 0)
        grid.addWidget(self.__lab9, 3, 0)
        grid.addWidget(self.__text, 2, 1)
        grid.addWidget(self.__text2, 3, 1)
        grid.addWidget(self.__text10, 5, 1)
        grid.addWidget(self.__text3, 2, 1, 1, 3)
        #self.__text.setText("127.0.0.1")
        self.__text2.setText("15001")
        self.__text3.setText("")
        grid.addWidget(self.__okcon, 4, 1)
        grid.addWidget(self.__okcom, 2, 4)
        grid.addWidget(self.__nouvelco, 0, 3)
        grid.addWidget(self.__deco, 0, 4)
        self.__deco.hide()
        self.__info.hide()
        self.__infohost.hide()
        self.__infoport.hide()
        self.__infoportlabel.hide()
        self.__infohostlabel.hide()
        self.__nouvelco.hide()
        self.__okcon.clicked.connect(self.okconnexion)
        self.__okcom.clicked.connect(self.okcommande)
        self.__deco.clicked.connect(self.deconnexion)
        self.__btnadd.clicked.connect(self.ajout)
        self.__okcom.hide()
        self.__lab9.hide()
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
        host = str(self.__text.currentText())
        port = int(self.__text2.text())
        self.__client = Client(host, port)
        self.__client.connexion()
        self.__okcon.setEnabled(False)
        self.__okcom.show()
        self.__lab3.show()
        self.__lab5.show()
        self.__infohost.show()
        self.__infoport.show()
        self.__infoport.setEnabled(False)
        self.__infohost.setEnabled(False)
        self.__infoportlabel.show()
        self.__infohostlabel.show()
        self.__text3.show()
        self.__text2.hide()
        self.__lab.hide()
        self.__info.show()
        self.__lab8.hide()
        self.__lab9.show()
        self.__text2.hide()
        self.__labtitre.hide()
        self.__okcon.hide()
        self.__deco.show()
        self.__nouvelco.show()
        self.__infoportlabel.setText(f" {self.__text2.text()}")
        self.__infohostlabel.setText(f" {self.__text.currentText()}")

    def ajout(self):
        file = open("OMG.txt.txt", "a")
        file.write(f"\n{self.__text10.text()}")

    def _actionQuitter(self):
        QCoreApplication.exit(0)

    def deconnexion(self):
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