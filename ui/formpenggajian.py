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

class formPenggajian(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formpenggajian.ui", self)
        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("penggajian")
        self.model = TableModel(data, headers)
        self.tablePenggajian.setModel(self.model)
        self.loadCmbKaryawan()

        # set button
        self.kodeKaryawanComboBox.activated.connect(self.setInputan)
        self.btnSimpan.clicked.connect(self.add_data)
        self.tablePenggajian.clicked.connect(self.on_table_click)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.btnCetak.clicked.connect(self.print_pdf)

    def loadCmbKaryawan(self):
        data, headers = KoneksiDB().fetch_all("karyawan")
        self.kodeKaryawanComboBox.addItem("Pilih Karyawan")
        for d in data:
            self.kodeKaryawanComboBox.addItem(f"{d[0]}/{d[2]}")

    def setCmbKdKaryawan(self, kdKaryawan):
        data, headers = KoneksiDB().fetch_all("karyawan")

        for d in data:
            if d[0] == kdKaryawan:
                self.kodeKaryawanComboBox.setCurrentText(f"{d[0]}/{d[2]}")

    def setInputan(self):
        if self.kodeKaryawanComboBox.currentText() != "Pilih Karyawan":
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]
            data, headers = KoneksiDB().getGajiBagian(kdKaryawan)
            self.gajiPokokLineEdit.setText(str(data[2]))
            self.tunjTransportasiLineEdit.setText(str(data[3]))
            self.tunjMakanLineEdit.setText(str(data[4]))
            self.totalLemburLineEdit.setText(str(data[5]))

    def clear_inputs(self):
        self.noPenggajianLineEdit.clear()
        self.noPenggajianLineEdit.setEnabled(True)
        self.periodeGajiLineEdit.clear()
        self.tanggalDateEdit.clear()
        self.kodeKaryawanComboBox.setCurrentText("Pilih Karyawan")
        self.gajiPokokLineEdit.clear()
        self.tunjTransportasiLineEdit.clear()
        self.tunjMakanLineEdit.clear()
        self.totalLemburLineEdit.clear()
        self.totalBonusLineEdit.clear()

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
            noPenggajian_value = str(record[0])
            periodeGaji_value = str(record[1])
            tanggal_value = str(record[2]).split("-")
            kdKaryawan_value = str(record[3])
            gajiPokok_value = str(record[4])
            tunjTransport_value = str(record[5])
            tunjMakan_value = str(record[6])
            totalLembur_value = str(record[7])
            totalBonus_value = str(record[8])

            # set inputan
            self.noPenggajianLineEdit.setText(noPenggajian_value)
            self.noPenggajianLineEdit.setEnabled(False)
            self.periodeGajiLineEdit.setText(periodeGaji_value)

            # set tanggal absen
            tahunAbsen = int(tanggal_value[0])
            bulanAbsen = int(tanggal_value[1])
            tanggalAbsen = int(tanggal_value[2])
            tglAbsenDate = QDate(tahunAbsen, bulanAbsen, tanggalAbsen)
            self.tanggalDateEdit.setDate(tglAbsenDate)

            # set kodebagian combo box
            self.setCmbKdKaryawan(kdKaryawan_value)

            self.gajiPokokLineEdit.setText(gajiPokok_value)
            self.tunjTransportasiLineEdit.setText(tunjTransport_value)
            self.tunjMakanLineEdit.setText(tunjMakan_value)
            self.totalLemburLineEdit.setText(totalLembur_value)
            self.totalBonusLineEdit.setText(totalBonus_value)

        except Exception as e:
            # Menangkap kesalahan dan mencetak pesan
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def load_data(self):
        try:
            data, headers = KoneksiDB().fetch_all("penggajian")
            self.model = TableModel(data, headers)
            self.tablePenggajian.setModel(self.model)
            # Pastikan 'table_view' adalah object name dari QTableView di Qt Designer
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def add_data(self):
        noPenggajian = self.noPenggajianLineEdit.text()
        periodeGaji = self.periodeGajiLineEdit.text()
        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else :
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        gajiPokok = self.gajiPokokLineEdit.text()
        tunjTransportasi = self.tunjTransportasiLineEdit.text()
        tunjMakan = self.tunjMakanLineEdit.text()
        totalLembur = self.totalLemburLineEdit.text()
        totalBonus = self.totalBonusLineEdit.text()

        if noPenggajian and periodeGaji and tanggal and kdKaryawan and gajiPokok and tunjTransportasi and tunjMakan and totalLembur and totalBonus :
            self.koneksiDB.tambah_penggajian(noPenggajian, periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus)
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            self.clear_inputs()
            self.load_data()

        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):
        noPenggajian = self.noPenggajianLineEdit.text()
        periodeGaji = self.periodeGajiLineEdit.text()
        tanggal = self.tanggalDateEdit.date().toString("yyyy-MM-dd")

        # cek apakah karyawan sudah dipilih
        if self.kodeKaryawanComboBox.currentText().split("/")[0] == "Pilih Karyawan":
            kdKaryawan = ""
        else:
            kdKaryawan = self.kodeKaryawanComboBox.currentText().split("/")[0]

        gajiPokok = self.gajiPokokLineEdit.text()
        tunjTransportasi = self.tunjTransportasiLineEdit.text()
        tunjMakan = self.tunjMakanLineEdit.text()
        totalLembur = self.totalLemburLineEdit.text()
        totalBonus = self.totalBonusLineEdit.text()

        if noPenggajian and periodeGaji and tanggal and kdKaryawan and gajiPokok and tunjTransportasi and tunjMakan and totalLembur and totalBonus:
            try:
                # Ubah data di database
                self.koneksiDB.ubah_penggajian(noPenggajian, periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.clear_inputs()
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        noPenggajian = self.noPenggajianLineEdit.text()
        self.koneksiDB.hapus_penggajian(noPenggajian)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
        self.load_data()
        self.clear_inputs()

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("penggajian")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "penggajian_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Judul
            c.drawString((width/2)-50, height - 50, "Laporan Data Penggajian")

            # Header tabel
            headers = ["No Penggajian", "Periode", "Tanggal", "KD Karyawan", "Gaji Pokok", "Tunj. Transport", "Tunj. Makan", "Total Lembur", "Total Bonus"]
            x_positions = [10, 70, 130, 190, 250, 310, 370, 430, 490]
            row_height = 20

            # Set font and size
            c.setFont("Helvetica", 9)

            # Draw header row
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y_position, header)
                c.rect(x_positions[i] - 5, y_position - 5, 60, row_height)  # Draw border

            # Menampilkan data
            y_position -= row_height
            for row in data:
                for i, cell in enumerate(row):
                    # Konversi tipe data date
                    if isinstance(cell, date):
                        cell = cell.strftime("%Y-%m-%d")

                    c.drawString(x_positions[i], y_position, str(cell))
                    c.rect(x_positions[i] - 5, y_position - 5, 60, row_height)  # Draw border
                y_position -= row_height  # Move to next row

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")