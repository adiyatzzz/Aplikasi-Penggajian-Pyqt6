from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6 import uic

class formAbsensi(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formabsensi.ui", self)
