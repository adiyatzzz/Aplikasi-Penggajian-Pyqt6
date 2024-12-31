import sys

from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6 import uic
from PyQt6.uic.Compiler.qtproxies import QtCore
from PyQt6.QtCore import QDate, QTime

from db.koneksi import KoneksiDB
from Model.TableModel import TableModel

from datetime import date, datetime, time, timedelta
# LIBRARY PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class formLembur(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formlembur.ui", self)

        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("lembur")
        self.model = TableModel(data, headers)
        self.tableLembur.setModel(self.model)
        self.loadCmbKaryawan()

        # set button
        self.btnSimpan.clicked.connect(self.add_data)
        self.tableLembur.clicked.connect(self.on_table_click)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.btnCetak.clicked.connect(self.print_pdf)

    def loadCmbKaryawan(self):
        data, headers = KoneksiDB().fetch_all("karyawan")
        self.kodeKaryawanComboBox.addItem("Pilih Karyawan")
        for d in data:
            self.kodeKaryawanComboBox.addItem(f"{d[0]}/{d[2]}")

    def load_data(self):
        try:
            data, headers = KoneksiDB().fetch_all("lembur")
            self.model = TableModel(data, headers)
            self.tableLembur.setModel(self.model)
            # Pastikan 'table_view' adalah object name dari QTableView di Qt Designer
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def clear_inputs(self):
        self.iDLemburLineEdit.clear()
        self.iDLemburLineEdit.setEnabled(True)
        self.kodeKaryawanComboBox.setCurrentText("Pilih Karyawan")
        self.tanggalDateEdit.clear()
        self.keteranganLineEdit.clear()

    def setCmbKdKaryawan(self, kdKaryawan):
        data, headers = KoneksiDB().fetch_all("karyawan")

        for d in data:
            if d[0] == kdKaryawan:
                self.kodeKaryawanComboBox.setCurrentText(f"{d[0]}/{d[2]}")

    def on_table_click(self, index):
        # Mendapatkan indeks baris yang diklik
        try:
            # Mendapatkan indeks baris yang diklik
            row = index.row()  # Mengambil nomor baris yang diklik
            column = index.column()  # Mengambil nomor kolom yang diklik

            # Ambil data dari model berdasarkan indeks
            record = self.model._data[row]

            # Ambil nilai dari kolom yang relevan
            idLembur_value = str(record[0])
            kdKaryawan_value = str(record[1])
            tanggal_value = str(record[2]).split("-")
            keterangan_value = str(record[3])


            # set inputan
            self.iDLemburLineEdit.setText(idLembur_value)
            self.iDLemburLineEdit.setEnabled(False)

            # set kodebagian combo box
            self.setCmbKdKaryawan(kdKaryawan_value)

            # set tanggal absen
            tahun = int(tanggal_value[0])
            bulan = int(tanggal_value[1])
            tanggal = int(tanggal_value[2])
            tglLembur = QDate(tahun, bulan, tanggal)
            self.tanggalDateEdit.setDate(tglLembur)

            self.keteranganLineEdit.setText(keterangan_value)

        except Exception as e:
            # Menangkap kesalahan dan mencetak pesan
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def add_data(self):
        idLembur = self.iDLemburLineEdit.text()

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else :
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")
        keterangan = self.keteranganLineEdit.text()


        if idLembur and kdKaryawan and tanggal and keterangan :
            self.koneksiDB.tambah_lembur(idLembur, kdKaryawan, tanggal, keterangan)
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        idLembur = self.iDLemburLineEdit.text()

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else:
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")
        keterangan = self.keteranganLineEdit.text()

        if idLembur and kdKaryawan and tanggal and keterangan :
            try:
                # Ubah data di database
                self.koneksiDB.ubah_lembur(idLembur, kdKaryawan, tanggal, keterangan)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.clear_inputs()
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        idLembur = self.iDLemburLineEdit.text()
        self.koneksiDB.hapus_lembur(idLembur)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
        self.load_data()
        self.clear_inputs()

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("lembur")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "lembur_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Judul
            c.drawString((width/2)-50, height - 50, "Laporan Data Lembur")

            # Header tabel
            headers = ["ID Lembur", "KD Karyawan", "Tanggal", "Keterangan"]
            x_positions = [110, 210, 310, 410, 510]
            row_height = 20

            # Draw header row
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y_position, header)
                c.rect(x_positions[i] - 5, y_position - 5, 100, row_height)  # Draw border

            # Menampilkan data
            y_position -= row_height
            for row in data:
                for i, cell in enumerate(row):
                    # Konversi tipe data date
                    if isinstance(cell, date):
                        cell = cell.strftime("%Y-%m-%d")

                    c.drawString(x_positions[i], y_position, str(cell))
                    c.rect(x_positions[i] - 5, y_position - 5, 100, row_height)  # Draw border
                y_position -= row_height  # Move to next row

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")