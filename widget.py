import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.theme = 'white'
        uic.loadUi('forn.ui', self)
        contacts = self.getLocalInfo()
        self.scrollArea.setWidgetResizable(True)

        for i in range(len(contacts)):
            name = QLabel(self, text=contacts[i][1])
            name.setStyleSheet('border-radius: 20%;'
                               'font-size: 20px;'
                               )
            pixmap = QPixmap('profile_images\\' + contacts[i][2])
            image = QLabel(self)
            image.setPixmap(pixmap)
            image.resize(60, 60)
            image.setStyleSheet('border-radius: 40%;')
            widget = QWidget(self)
            image.setParent(widget)
            name.setParent(widget)
            name.move(60, 10)
            widget.setParent(self.scrollAreaWidgetContents)
            widget.resize(350, 60)
            widget.move(10, 10 + 65 * i)
            widget.setStyleSheet('border: 2px solid black;'
                                 'border-radius: 30%;'
                                 'font-size: 20px;'
                                 f'background-color: {self.theme};')
        self.verticalScrollBar.setWidget(self.scrollAreaWidgetContents)
        self.scrollArea.setFixedHeight(400)
    def getLocalInfo(self):
        connection = sqlite3.connect("local_database.db")
        cursor = connection.cursor()
        contacts = list(cursor.execute("SELECT * FROM contacts;").fetchall())
        connection.close()
        return contacts

    def getNetworkInfo(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec())
