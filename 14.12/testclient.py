import socket, threading, sys
import sys
import pathlib
from threading import Lock
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QInputDialog
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
        self.setWindowIcon(QtGui.QIcon("oeil.png"))
        self.__labtitre = QLabel("Bienvenue sur Surveil'App !\n")
        self.__labsub2titre = QLabel("Informations")
        self.__lab = QLabel("Host")
        self.__lab8 = QLabel("Port")
        self.__labadd = QLabel("Ajout IP")
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
        self.__labvide = QLabel("")
        self.__labsubtitre = QLabel("Paramètres")
        self.__labsubtitre.setFont(QFont('Arial', 15))
        self.__labsub2titre.setFont(QFont('Arial', 15))
        # self.__labsubtitre.setAlignment(Qt.AlignCenter)
        self.__text = QComboBox()
        self.__text2 = QLineEdit("")
        self.__text3 = QLineEdit("")
        self.__text11 = QLineEdit("")
        self.__savefichier = QLineEdit("")
        self.__infohost = QLineEdit("")
        self.__infoport = QLineEdit("")
        self.__infoportlabel = QLabel("")
        self.__infohostlabel = QLabel("")
        self.__text10.hide()
        self.__labadd.hide()
        self.__btnadd.hide()
        self.__savefichier.hide()
        self.__btnadd.setEnabled(False)
        self.__w = None




        self.__client = None
        self.__okcon = QPushButton("Connexion")
        self.__okcom = QPushButton("Envoyer")
        self.__deco = QPushButton("Déconnexion")
        self.__nouvelco = QPushButton("Nouvel Co.")
        self.__fichiername = QPushButton("Choisir...")

        # Using readlines()
        self.__text11.setReadOnly(True)
        self.__lab3.hide()
        self.__lab5.hide()
        self.__text3.hide()
        self.__labnomfichier = QLabel("Fichier Source")
        grid.addWidget(self.__labsub2titre, 1, 0)
        grid.addWidget(self.__labtitre, 0, 1)
        grid.addWidget(self.__info, 0, 0)
        grid.addWidget(self.__labadd, 9, 0)
        grid.addWidget(self.__labvide, 6, 0)
        grid.addWidget(self.__btnadd, 9, 2)
        grid.addWidget(self.__infohost, 0, 1)
        grid.addWidget(self.__infoport, 0, 2)
        grid.addWidget(self.__infoportlabel, 0, 2)
        grid.addWidget(self.__infohostlabel, 0, 1)
        grid.addWidget(self.__lab3, 3, 0, 1, 5)
        grid.addWidget(self.__lab2, 4, 1)
        grid.addWidget(self.__labsubtitre, 7, 0)
        grid.addWidget(self.__lab4, 1, 1)
        grid.addWidget(self.__lab, 2, 0)
        grid.addWidget(self.__lab8, 3, 0)
        grid.addWidget(self.__lab5, 2, 0)
        grid.addWidget(self.__lab9, 3, 0)
        grid.addWidget(self.__text, 2, 1)
        grid.addWidget(self.__text2, 3, 1)
        grid.addWidget(self.__text10, 9, 1)
        self.__text3.setPlaceholderText("Entrez votre commande ici")
        grid.addWidget(self.__text3, 2, 1, 1, 3)
        #self.__text.setText("127.0.0.1")
        self.__text2.setText("10007")
        self.__text3.setText("")
        self.__text10.setPlaceholderText("Entrez une IP à ajouter")
        self.__lab3.setReadOnly(True)
        grid.addWidget(self.__okcon, 4, 1)
        grid.addWidget(self.__okcom, 2, 4)
        grid.addWidget(self.__nouvelco, 0, 3)
        grid.addWidget(self.__deco, 0, 4)
        grid.addWidget(self.__labnomfichier, 8, 0)
        grid.addWidget(self.__text11, 8, 1)
        grid.addWidget(self.__fichiername, 8, 2)
        grid.addWidget(self.__savefichier, 10, 2)
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
        self.__nouvelco.clicked.connect(self.nouvelco)
        self.__btnadd.clicked.connect(self.ajout)
        self.__fichiername.clicked.connect(self.fichiernom)
        self.__okcom.hide()
        self.__lab9.hide()
        self.__okcon.setEnabled(False)
        # self.__text11.setText(f"OMG.txt")



        self.setWindowTitle("Application - Surveillance")


    def okcommande(self):
        msg = self.__text3.text()
        try:
            reponse = self.__client.envoi(msg)
        except:
            self.__lab3.append(f"[Erreur] Le serveur ne répond pas ! Vérifier quil soit lancé et fonctionnel\n")
        else:
            self.__lab3.append(f"{reponse}\n")





    def fichiernom(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self, "Choisissez votre fichier", "",
                                                      "Fichiers Texte (*.txt)", options=options)

            testest = pathlib.Path(fileName).name
            self.__text11.setText(fileName)
            file1 = open(f"{testest}", 'r')
            Lines = file1.readlines()

            count = 0
            # Strips the newline character
            for line in Lines:
                count += 1
                self.__text.addItem(line.strip())
            self.__btnadd.setEnabled(True)
            self.__text10.show()
            self.__labadd.show()
            self.__btnadd.show()
            self.__okcon.setEnabled(True)
        except:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Erreur ! Vous avez fermer la fenêtre sans selectionner de fichier ")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()





    def nouvelco(self):
        self.__w = MainWindow()
        self.__w.show()




    def okconnexion(self):
        # self.__lab2.setText(f"Host / Port : {self.__text.text()} | {self.__text2.text()}")
        host = str(self.__text.currentText())
        port = int(self.__text2.text())
        self.__client = Client(host, port)
        self.__labsubtitre.hide()
        self.__client.connexion()
        self.__okcon.setEnabled(False)
        self.__okcom.show()
        self.__lab3.show()
        self.__lab5.show()
        self.__labsub2titre.hide()
        self.__infohost.show()
        self.__infoport.show()
        self.__infoport.setEnabled(False)
        self.__infohost.setEnabled(False)
        self.__infoportlabel.show()
        self.__infohostlabel.show()
        self.__text3.show()
        self.__text2.hide()
        self.__lab.hide()
        self.__btnadd.hide()
        self.__labadd.hide()
        self.__info.show()
        self.__lab8.hide()
        # self.__lab9.show()
        self.__text2.hide()
        self.__text10.hide()
        self.__labtitre.hide()
        self.__okcon.hide()
        self.__deco.show()
        self.__nouvelco.show()



        self.__text11.hide()
        self.__labnomfichier.hide()
        self.__fichiername.hide()

        self.__infoportlabel.setText(f" {self.__text2.text()}")
        self.__infohostlabel.setText(f" {self.__text.currentText()}")

    def ajout(self):
        if self.__text10.text() != "":
            testest = self.__text11.text()
            file = open(f"{testest}", "a")
            file.write(f"\n{self.__text10.text()}")
            self.__text.addItem(self.__text10.text())
            self.__text10.setText("")
            self.__savefichier = self.__text11.text()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Erreur")
            msg.setText("Impossible d'ajouter un host vide")
            msg.setIcon(QMessageBox.Critical)
            x = msg.exec_()






    def _actionQuitter(self):
        QCoreApplication.exit(0)

    def deconnexion(self):
        self.__client.envoi("disconnect")
        self.__client.envoi("disconnect")
        QCoreApplication.exit(0)

    #
    # def deconnexion(self):
    #     self.__client.envoi("disconnect")
    #
    #     # self.__lab2.setText(f"Host / Port : {self.__text.text()} | {self.__text2.text()}")
    #
    #     self.__labsubtitre.show()
    #
    #
    #     self.__okcom.hide()
    #     self.__lab3.hide()
    #     self.__lab5.hide()
    #
    #
    #     self.__labsub2titre.show()
    #     self.__infohost.hide()
    #     self.__infoport.hide()
    #
    #     self.__infoportlabel.hide()
    #     self.__infohostlabel.hide()
    #     self.__text3.hide()
    #     self.__text2.show()
    #     self.__lab.show()
    #     self.__btnadd.show()
    #     self.__labadd.show()
    #     self.__info.hide()
    #     self.__lab8.show()
    #
    #     self.__text2.show()
    #     self.__text10.show()
    #     self.__labtitre.show()
    #     self.__okcon.show()
    #     self.__deco.hide()
    #     self.__nouvelco.hide()
    #
    #     self.__text11.show()
    #     self.__labnomfichier.show()
    #     self.__fichiername.show()





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