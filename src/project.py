import sys

from PyQt5.QtWidgets import QApplication

from interface import basicWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = basicWindow()
    windowExample.show()
    sys.exit(app.exec_())
