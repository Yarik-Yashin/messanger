import sys
from widgets import QApplication, Login, Registration, Interface

app = QApplication(sys.argv)
ex = Login()
ex.show()
sys.exit(app.exec_())
