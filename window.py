from window_ui import Ui_MainWindow

from PySide import QtCore, QtGui
from PySide.QtCore import Qt

import math

FRAME_TIME_MS = 33
VIEW_HEIGHT = 20.0

class Window(QtGui.QMainWindow):
    def __init__(self, simulator, parent=None):
        super(Window, self).__init__(parent)

        self.simulator = simulator

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.canvas.paintEvent = self.on_canvas_paint_event
        self.ui.canvas.resizeEvent = self.on_canvas_resize_event

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_timeout)
        self.timer.start(FRAME_TIME_MS)

        self.set_simulator_bounds()

    def on_canvas_paint_event(self, event):
        painter = QtGui.QPainter(self.ui.canvas)
        pixel_scale = self.ui.canvas.height() / VIEW_HEIGHT
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0), 2, Qt.SolidLine, Qt.SquareCap, Qt.MiterJoin)
        brush = QtGui.QBrush(QtGui.QColor(0xE0, 0xF0, 0xFF))
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        for circle in self.simulator.circles:
            x = circle.position.x * pixel_scale + self.ui.canvas.width() / 2
            y = circle.position.y * pixel_scale + self.ui.canvas.height() / 2
            radius = circle.radius * pixel_scale
            painter.drawEllipse(QtCore.QPoint(x, y), radius, radius)

        for polygon in self.simulator.polygons:
            brush = QtGui.QBrush(QtGui.QColor(0xE0, 0xF0, 0xFF))
            painter.setBrush(brush)

            points = []
            for point in polygon.transformed_points():
                x = point.x * pixel_scale + self.ui.canvas.width() / 2
                y = point.y * pixel_scale + self.ui.canvas.height() / 2
                points.append(QtCore.QPoint(x, y))

            painter.drawPolygon(points)

    def on_canvas_resize_event(self, event):
        self.set_simulator_bounds()

    def set_simulator_bounds(self):
        unit_scale = VIEW_HEIGHT / self.ui.canvas.height()
        min_x = -self.ui.canvas.width() * unit_scale / 2 + 1
        min_y = -VIEW_HEIGHT / 2 + 1
        max_x = -min_x
        max_y = -min_y
        self.simulator.set_bounds(min_x, min_y, max_x, max_y)

    def on_timeout(self):
        self.simulator.advance(FRAME_TIME_MS / 1000.0)
        self.update()
