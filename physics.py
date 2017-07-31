#! /usr/bin/env python

from window import Ui_MainWindow

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt

import sys

class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canvas.paintEvent = self.onCanvasPaintEvent
        self.rotation = 0

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.onTimeout)
        self.timer.start(20)

    def onCanvasPaintEvent(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        painter.setPen(QtGui.QPen(QtGui.QColor(0xff, 0, 0), 3, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin))
        painter.translate(300, 300);
        painter.rotate(self.rotation)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawRect(-50, -50, 100, 100)

    def onTimeout(self):
        self.rotation += 1;
        self.update()
 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    window = Window()
    window.show()

    ret = app.exec_()

    sys.exit(ret)
