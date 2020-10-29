from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtCore, QtMultimedia, QtGui, uic
from PyQt5.QtGui import QCursor
import requests
import json


class Interface(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.theme = 'white'
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 700)

        """Левая часть """
        self.contacts = self.getContacts()
        self.scroll = QScrollArea(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        for i in range(len(self.contacts)):
            name = QLabel(self, text=self.contacts[i][0])
            name.setStyleSheet('border-radius: 20%;'
                               'font-size: 20px;'
                               )
            pixmap = QPixmap(self.contacts[i][1].replace("'", ""))
            image = QLabel(self)
            image.setPixmap(pixmap)
            image.resize(60, 60)
            image.setStyleSheet('border-radius: 30%;')
            button = QPushButton(text='Перейти к диалогу')
            widget = QWidget(self)
            button.setParent(widget)
            image.setParent(widget)
            name.setParent(widget)
            name.move(60, 10)
            button.move(10, 60)
            button.setEnabled(True)
            button.clicked.connect(self.toDialog)
            widget.setStyleSheet('border: 2px solid black;'
                                 'border-radius: 30%;'
                                 'font-size: 20px;'
                                 'padding: 3%;'
                                 f'background-color: {self.theme};')
            widget.setFixedSize(350, 100)
            self.vbox.addWidget(widget)
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.setCentralWidget(self.scroll)
        self.scroll.setStyleSheet('border: 2px solid black')
        self.scroll.setFixedSize(400, 600)
        self.new_contact_field = QLineEdit(self)
        self.new_contact_field.move(0, 620)
        self.new_contact_field.resize(380, 80)
        self.label_of_new_contact = QLabel(self, text='Введите имя нового контакта')
        self.label_of_new_contact.move(0, 600)
        self.label_of_new_contact.resize(400, 20)
        self.button_new_contact = QPushButton(self, text='✓')
        self.button_new_contact.move(380, 620)
        self.button_new_contact.resize(20, 80)
        self.button_new_contact.clicked.connect(self.addContact)
        """Левая часть ^"""

        """Правая часть"""
        self.scroll2 = QScrollArea(self)
        self.widget2 = QWidget()
        self.vbox2 = QVBoxLayout()
        self.startLabel = QLabel(text='Собеседник не выбран')
        self.startLabel.setStyleSheet('font-size: 36px;')
        self.vbox2.addWidget(self.startLabel)
        self.widget2.setLayout(self.vbox2)
        self.scroll2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll2.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setWidget(self.widget2)
        self.scroll2.setStyleSheet('border: 2px solid black')
        self.scroll2.setFixedSize(600, 600)
        self.scroll2.move(400, 0)
        """Правая часть^"""

    def getContacts(self):
        a = requests.post('http://127.0.0.1:5000/contacts', data={'name': self.name}).text
        a = json.loads(a)
        list_of_contacts = list()
        for i in a:
            list_of_contacts.append(a[i])
        return list_of_contacts

    def toDialog(self):
        print('Test')

    def addContact(self):
        a = requests.post('http://127.0.0.1:5000/add_contact',
                          data={'name': self.name, 'contact_name': self.new_contact_field.text()})
        new_contacts = list(filter(lambda x: x not in self.contacts, self.getContacts()))

        print(new_contacts)
        for i in range(len(new_contacts)):
            name = QLabel(self, text=new_contacts[i][0])
            name.setStyleSheet('border-radius: 20%;'
                               'font-size: 20px;'
                               )
            pixmap = QPixmap(new_contacts[i][1].replace("'", ""))
            image = QLabel(self)
            image.setPixmap(pixmap)
            image.resize(60, 60)
            image.setStyleSheet('border-radius: 30%;')
            button = QPushButton(text='Перейти к диалогу')
            widget = QWidget(self)
            button.setParent(widget)
            image.setParent(widget)
            name.setParent(widget)
            name.move(60, 10)
            button.move(10, 60)
            button.setEnabled(True)
            button.clicked.connect(self.toDialog)
            widget.setStyleSheet('border: 2px solid black;'
                                 'border-radius: 30%;'
                                 'font-size: 20px;'
                                 'padding: 3%;'
                                 f'background-color: {self.theme};')
            widget.setFixedSize(350, 100)
            self.vbox.addWidget(widget)
        self.new_contact_field.setText('')
        self.contacts = self.getContacts()


class ClickLabel(QLabel):
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class Registration(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('reg.ui', self)
        self.label_3 = ClickLabel(self, text='Уже зарегистрированы ? Войти')
        self.label_3.setStyleSheet('font-size: 16px;'
                                   'color: blue;')
        self.label_3.resize(281, 41)
        self.label_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_3.clicked.connect(self.toLogin)
        self.label_3.move(30, 240)
        self.label_3.setAlignment((QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop))
        self.pushButton.clicked.connect(self.checkForm)

    def checkForm(self):
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and \
                self.lineEdit_2.text() == self.lineEdit_3.text():
            a = requests.post(data={'login': self.lineEdit.text(), 'password': self.lineEdit_2.text()},
                              url='http://127.0.0.1:5000/registration').text
            if a == 'Ok':
                self.name = self.lineEdit.text()
                global ex
                ex = Interface(name=self.name)
                ex.show()
                self.close()

    def toLogin(self):
        global ex
        ex = Login()
        ex.show()
        self.close()


class Login(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('login.ui', self)
        self.is_auth = False
        self.label_3 = ClickLabel(self, text='Нет акканута ? Зарегистрироваться')
        self.label_3.setStyleSheet('font-size: 16px;'
                                   'color: blue;')
        self.label_3.resize(281, 41)
        self.label_3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.label_3.clicked.connect(self.toRegistration)
        self.label_3.move(30, 190)
        self.label_3.setAlignment((QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop))
        self.pushButton.clicked.connect(self.checkForm)

    def checkForm(self):
        if self.lineEdit.text() and self.lineEdit_2.text():
            a = requests.post(data={'login': self.lineEdit.text(), 'password': self.lineEdit_2.text()},
                              url='http://127.0.0.1:5000/login').text
            if a == 'Ok':
                self.name = self.lineEdit.text()
                global ex
                ex = Interface(name=self.name)
                ex.show()
                self.close()

    def toRegistration(self):
        global ex2
        ex2 = Registration()
        ex2.show()
        self.close()
