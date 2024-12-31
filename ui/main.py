from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
import sys
from PyQt6 import uic

from formkaryawan import formKaryawan
from formbagian import formBagian
from formabsensi import formAbsensi
from formlembur import formLembur
from formpenggajian import formPenggajian


class Main(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        # set button menu
        self.btnFormKaryawan = self.findChild(QPushButton, "btnFormKaryawan")
        self.btnFormKaryawan.clicked.connect(self.tampilFormKaryawan)

        self.btnFormBagian = self.findChild(QPushButton, "btnFormBagian")
        self.btnFormBagian.clicked.connect(self.tampilFormBagian)

        self.btnFormAbsensi = self.findChild(QPushButton, "btnFormAbsensi")
        self.btnFormAbsensi.clicked.connect(self.tampilFormAbsensi)

        self.btnFormLembur = self.findChild(QPushButton, "btnFormLembur")
        self.btnFormLembur.clicked.connect(self.tampilFormLembur)

        self.btnFormPenggajian = self.findChild(QPushButton, "btnFormPenggajian")
        self.btnFormPenggajian.clicked.connect(self.tampilFormPenggajian)

    def tampilFormKaryawan(self):
        self.formKaryawan = formKaryawan()
        self.formKaryawan.show()

    def tampilFormBagian(self):
        self.formBagian = formBagian()
        self.formBagian.show()

    def tampilFormAbsensi(self):
        self.formAbsensi = formAbsensi()
        self.formAbsensi.show()

    def tampilFormLembur(self):
        self.formLembur = formLembur()
        self.formLembur.show()

    def tampilFormPenggajian(self):
        self.formPenggajian = formPenggajian()
        self.formPenggajian.show()

if __name__ == "__main__":
    aplikasi = QApplication(sys.argv)
    tampilForm = Main()
    tampilForm.show()
    sys.exit(aplikasi.exec())