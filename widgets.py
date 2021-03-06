from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtMultimedia, QtGui, uic
from PyQt5.QtGui import QCursor
import requests
import json


class Interface(QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 700)

        """Левая часть """
        self.contacts = self.getContacts()  # Получаем список контактов
        self.scroll = QScrollArea(self)
        self.widget = QWidget()
        self.vbox = QVBoxLayout()  # Создаем сетку для размещения на ней контактов
        for i in range(len(self.contacts)):
            name = QLabel(self, text=self.contacts[i][0])
            name.setStyleSheet('border-radius: 20%;'
                               'font-size: 20px;'
                               )
            button = QPushButton(text='Перейти к диалогу')
            widget = QWidget(self)  # Создаем виджет, на который крепим кнопку и имя
            button.setParent(widget)
            name.setParent(widget)
            name.move(60, 10)
            button.move(10, 60)
            button.setEnabled(True)
            button.clicked.connect(self.toDialog)
            widget.setStyleSheet('border: 2px solid black;'
                                 'border-radius: 30%;'
                                 'font-size: 20px;'
                                 'padding: 3%;')
            widget.setFixedSize(350, 100)
            self.vbox.addWidget(widget)  # Прикрепляем виджет к сетке
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
        self.newMessageField = QLineEdit(self)
        self.newMessageField.move(400, 620)
        self.newMessageField.resize(380, 80)
        self.button_new_message = QPushButton(self, text='✓')
        self.button_new_message.move(780, 620)
        self.button_new_message.resize(20, 80)
        self.button_new_message.clicked.connect(self.sendMessage)
        self.label_of_new_message = QLabel(self, text='Введите сообщение')
        self.label_of_new_message.move(400, 600)
        self.label_of_new_message.resize(400, 20)
        """Правая часть^"""
        # Создаем таймер для проверки новых сообщений
        self.timer = QTimer()
        self.timer.setInterval(100000)
        self.timer.timeout.connect(self.toDialog)
        self.timer.start()

    def getContacts(self):
        # Функция для получения списка контактов
        a = requests.post('https://f535f8e21008.ngrok.io/contacts', data={'name': self.name}).text
        a = json.loads(a)
        list_of_contacts = list()
        for i in a:
            list_of_contacts.append(a[i])
        return list_of_contacts

    def toDialog(self):
        # Функция для перехода к диалогу
        try:
            if not self.sender().parent().children()[1].text():
                send = self.last_sender
                self.last_sender = send
            else:
                send = self.sender()
                self.last_sender = send
        except AttributeError:
            try:
                send = self.last_sender
            except AttributeError:
                return
        for i in range(self.vbox2.count()):
            self.vbox2.itemAt(i).widget().close()
        try:
            self.startLabel.setText('')
            self.vbox2.removeWidget(self.startLabel)
            del self.startLabel
        except AttributeError:
            pass
        getter = send.parent().children()[1].text()
        self.getter = getter
        sender = self.name
        messages = self.getMessages(name=sender, contact_name=getter)
        for i in messages:
            widget = QWidget(self)

            label = QLabel(text=i[3])
            label.setParent(widget)
            label.move(20, 20)
            name_label_text = requests.post('https://f535f8e21008.ngrok.io/getName', {'id': i[1]}).text
            name_label = QLabel(text=name_label_text)
            name_label.setParent(widget)
            widget.setStyleSheet('background-color:whitesmoke;'
                                 'border: 1px solid black;'
                                 'margin-left: 10px;')
            label.setStyleSheet('border: initial;')
            widget.setFixedSize(400, 70)
            self.vbox2.addWidget(widget)

    def addContact(self):
        # Функция для добавления контактов
        requests.post('https://f535f8e21008.ngrok.io/add_contact',
                      data={'name': self.name, 'contact_name': self.new_contact_field.text()})
        new_contacts = list(filter(lambda x: x not in self.contacts, self.getContacts()))

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

    def getMessages(self, name, contact_name):
        # Функция для получения сообщений
        messages = requests.post('https://f535f8e21008.ngrok.io/getMessages', {'name': name, 'contact_name': contact_name}).text
        messages = json.loads(messages)
        return_list = list()
        for i in messages:
            return_list.append(messages[i])
        return return_list

    def sendMessage(self):
        # Функция для отправки сообщений
        try:
            requests.post('https://f535f8e21008.ngrok.io/sendMessage',
                          {'login': self.name, 'contact_name': self.getter, 'text': self.newMessageField.text()})
            self.toDialog()
            self.newMessageField.setText('')

        except AttributeError:
            pass


class ClickLabel(QLabel):
    # Класс для кликабельных надписей
    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)


class Registration(QMainWindow):
    # Класс регистрации
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
                              url='https://f535f8e21008.ngrok.io/registration').text
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
    # Класс авторизации
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
                              url='https://f535f8e21008.ngrok.io/login').text
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
