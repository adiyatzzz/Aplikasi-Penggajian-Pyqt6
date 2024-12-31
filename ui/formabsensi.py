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

class formAbsensi(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formabsensi.ui", self)
        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("absensi")
        self.model = TableModel(data, headers)
        self.tableAbsen.setModel(self.model)
        self.loadCmbKaryawan()

        # set button
        self.btnSimpan.clicked.connect(self.add_data)
        self.tableAbsen.clicked.connect(self.on_table_click)
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
            data, headers = KoneksiDB().fetch_all("absensi")
            self.model = TableModel(data, headers)
            self.tableAbsen.setModel(self.model)
            # Pastikan 'table_view' adalah object name dari QTableView di Qt Designer
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def clear_inputs(self):
        self.iDAbsensiLineEdit.clear()
        self.iDAbsensiLineEdit.setEnabled(True)
        self.kodeKaryawanComboBox.setCurrentText("Pilih Karyawan")
        self.tanggalDateEdit.clear()
        self.jamMasukTimeEdit.clear()
        self.jamKeluarTimeEdit.clear()
        self.statusKehadiranComboBox.setCurrentText("Pilih Kehadiran")
        self.jenisKerjaLineEdit.clear()
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
            idAbsen_value = str(record[0])
            kdKaryawan_value = str(record[1])
            tanggal_value = str(record[2]).split("-")
            jamMasuk_value = str(record[3]).split(":")
            jamKeluar_value = str(record[4]).split(":")
            statusKehadiran_value = str(record[5])
            jenisKerja_value = str(record[6])
            keterangan_value = str(record[7])

            # set inputan
            self.iDAbsensiLineEdit.setText(idAbsen_value)
            self.iDAbsensiLineEdit.setEnabled(False)

            # set kodebagian combo box
            self.setCmbKdKaryawan(kdKaryawan_value)

            # set tanggal absen
            tahunAbsen = int(tanggal_value[0])
            bulanAbsen = int(tanggal_value[1])
            tanggalAbsen = int(tanggal_value[2])
            tglAbsenDate = QDate(tahunAbsen, bulanAbsen, tanggalAbsen)
            tglAbsenDate = QDate(tahunAbsen, bulanAbsen, tanggalAbsen)
            self.tanggalDateEdit.setDate(tglAbsenDate)

            # waktu masuk
            jamMasuk = int(jamMasuk_value[0])
            menitMasuk = int(jamMasuk_value[1])
            detikMasuk = int(jamMasuk_value[2])
            waktuMasuk = QTime(jamMasuk, menitMasuk, detikMasuk)
            self.jamMasukTimeEdit.setTime(waktuMasuk)

            # waktu keluar
            jamKeluar = int(jamKeluar_value[0])
            menitKeluar = int(jamKeluar_value[1])
            detikKeluar = int(jamKeluar_value[2])
            waktuKeluar = QTime(jamKeluar, menitKeluar, detikKeluar)
            self.jamKeluarTimeEdit.setTime(waktuKeluar)

            self.statusKehadiranComboBox.setCurrentText(statusKehadiran_value)
            self.jenisKerjaLineEdit.setText(jenisKerja_value)
            self.keteranganLineEdit.setText(keterangan_value)

        except Exception as e:
            # Menangkap kesalahan dan mencetak pesan
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def add_data(self):
        idAbsensi = self.iDAbsensiLineEdit.text()

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else :
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")
        jamMasuk = self.jamMasukTimeEdit.time().toString("HH:mm:ss")
        jamKeluar = self.jamKeluarTimeEdit.time().toString("HH:mm:ss")

        # cek apakah kehadiran sudah dipilih
        if self.statusKehadiranComboBox.currentText() == "Pilih Kehadiran":
            kehadiran = ""
        else:
            kehadiran = self.statusKehadiranComboBox.currentText()

        jenisKerja = self.jenisKerjaLineEdit.text()
        keterangan = self.keteranganLineEdit.text()


        if idAbsensi and kdKaryawan and tanggal and jamMasuk and jamKeluar and kehadiran and jenisKerja and keterangan :
            self.koneksiDB.tambah_absensi(idAbsensi, kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan)
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            self.clear_inputs()
            self.load_data()

        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):

        idAbsensi = self.iDAbsensiLineEdit.text()

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else:
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")
        jamMasuk = self.jamMasukTimeEdit.time().toString("HH:mm:ss")
        jamKeluar = self.jamKeluarTimeEdit.time().toString("HH:mm:ss")

        # cek apakah kehadiran sudah dipilih
        if self.statusKehadiranComboBox.currentText() == "Pilih Kehadiran":
            kehadiran = ""
        else:
            kehadiran = self.statusKehadiranComboBox.currentText()

        jenisKerja = self.jenisKerjaLineEdit.text()
        keterangan = self.keteranganLineEdit.text()

        if idAbsensi and kdKaryawan and tanggal and jamMasuk and jamKeluar and kehadiran and jenisKerja and keterangan:
            try:
                # Ubah data di database
                self.koneksiDB.ubah_absensi(idAbsensi, kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.clear_inputs()
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        idAbsensi = self.iDAbsensiLineEdit.text()
        self.koneksiDB.hapus_absensi(idAbsensi)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
        self.load_data()
        self.clear_inputs()

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("absensi")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "absensi_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Judul
            c.drawString((width/2)-50, height - 50, "Laporan Data Absensi")

            # Set font and size
            c.setFont("Helvetica", 9)

            # Header tabel
            headers = ["ID Absen", "KD Karyawan", "Tanggal", "Jam Masuk", "Jam Keluar", "Status", "Jenis Kerja", "Keterangan"]
            x_positions = [10, 80, 150, 220, 290, 360, 430, 500]
            row_height = 20

            # Draw header row
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y_position, header)
                c.rect(x_positions[i] - 5, y_position - 5, 70, row_height)  # Draw border

            # Menampilkan data
            y_position -= row_height
            for row in data:
                for i, cell in enumerate(row):
                    # Konversi tipe data date
                    if isinstance(cell, date):
                        cell = cell.strftime("%Y-%m-%d")
                    # Konversi tipe data timedelta
                    elif isinstance(cell, timedelta):
                        total_seconds = int(cell.total_seconds())
                        hours = (total_seconds % 86400) // 3600
                        minutes = (total_seconds % 3600) // 60
                        seconds = total_seconds % 60
                        cell = f"{hours:02}:{minutes:02}:{seconds:02}"

                    c.drawString(x_positions[i], y_position, str(cell))
                    c.rect(x_positions[i] - 5, y_position - 5, 70, row_height)  # Draw border
                y_position -= row_height  # Move to next row

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")