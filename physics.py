#! /usr/bin/env python

from window import Ui_MainWindow

from PyQt4 import QtCore, QtGui

import sys

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = Window()
    window.show()

    ret = app.exec_()

    sys.exit(ret)
