import sys

from QtractWindow import QtractWindow
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QtractWindow()
    window.show()
    sys.exit(app.exec_())
