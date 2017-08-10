#! /usr/bin/env python

from PySide import QtGui
import sys

import config, window

app = QtGui.QApplication(sys.argv)

window = window.Window(config.create_simulator())
window.show()

ret = app.exec_()

sys.exit(ret)
