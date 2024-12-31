import sys

from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6 import uic
from PyQt6.uic.Compiler.qtproxies import QtCore
from PyQt6.QtCore import QDate

from db.koneksi import KoneksiDB
from Model.TableModel import TableModel

from datetime import date, datetime, time, timedelta

# LIBRARY PDF
from reportlab.lib.pagesizes import letter, landscape, legal
from reportlab.pdfgen import canvas

class formKaryawan(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formkaryawan.ui", self)

        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("karyawan")
        self.model = TableModel(data, headers)
        self.tableKaryawan.setModel(self.model)

        # set combo box kdBagian
        self.loadDataBagian()

        # menyambungkan fungsi ke tombol
        self.btnSimpan.clicked.connect(self.add_data)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.tableKaryawan.clicked.connect(self.on_table_click)
        self.btnCetak.clicked.connect(self.print_pdf)

    def load_data(self):
        try:
            data, headers = KoneksiDB().fetch_all("karyawan")
            self.model = TableModel(data, headers)
            self.tableKaryawan.setModel(self.model)
            # Pastikan 'table_view' adalah object name dari QTableView di Qt Designer
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def loadDataBagian(self):
        data, headers = KoneksiDB().fetch_all("bagian")

        # for kd_bagian, nm_bagian in data:
        for d in data:
            self.kodeBagianComboBox.addItem(f"{d[0]}/{d[1]}")

    def setCmbKodeBagian(self, kdBagian):
        data, headers = KoneksiDB().fetch_all("bagian")

        # for kd_bagian, nm_bagian in data:
        for d in data:
            if d[0] == kdBagian:
                self.kodeBagianComboBox.setCurrentText(f"{d[0]}/{d[1]}")

    def on_table_click(self, index):
        # Mendapatkan indeks baris yang diklik
        try:
            # Mendapatkan indeks baris yang diklik
            row = index.row()  # Mengambil nomor baris yang diklik
            column = index.column()  # Mengambil nomor kolom yang diklik

            # Ambil data dari model berdasarkan indeks
            record = self.model._data[row]

            # Ambil nilai dari kolom yang relevan
            kdKaryawan_value = str(record[0])
            nik_value = str(record[1])
            nmKaryawan_value = str(record[2])
            kdBagian_value = str(record[3])
            kelamin_value = str(record[4])
            agama_value = str(record[5])
            alamatTinggal_value = str(record[6])
            noTelepon_value = str(record[7])
            tempatLahir_value = str(record[8])
            tglLahir_value = str(record[9]).split("-")
            statusKawin_value = str(record[10])
            tglMasuk_value = str(record[11]).split("-")

            self.kodeKaryawanLineEdit.setText(kdKaryawan_value)
            self.kodeKaryawanLineEdit.setEnabled(False)
            self.nIKLineEdit.setText(nik_value)
            self.namaKaryawanLineEdit.setText(nmKaryawan_value)

            # set kodebagian combo box
            self.setCmbKodeBagian(kdBagian_value)

            # set checked radio
            if kelamin_value == "Laki - Laki":
                self.lakiRadio.setChecked(True)
                self.perempuanRadio.setChecked(False)
            else:
                self.lakiRadio.setChecked(False)
                self.perempuanRadio.setChecked(True)

            self.agamaLineEdit.setText(agama_value)
            self.alamatLineEdit.setText(alamatTinggal_value)
            self.noTelponLineEdit.setText(noTelepon_value)
            self.tempatLahirLineEdit.setText(tempatLahir_value)
            # set tanggal lahir
            tahunLahir = int(tglLahir_value[0])
            bulanLahir = int(tglLahir_value[1])
            tanggalLahir = int(tglLahir_value[2])
            tglLahirDate = QDate(tahunLahir, bulanLahir, tanggalLahir)
            self.tanggalLahirDateEdit.setDate(tglLahirDate)

            self.statusKawinComboBox.setCurrentText(statusKawin_value)

            # Set Tanggal Masuk
            tahunMasuk = int(tglMasuk_value[0])
            bulanMasuk = int(tglMasuk_value[1])
            tanggalMasuk = int(tglMasuk_value[2])
            tglMasukDate = QDate(tahunMasuk, bulanMasuk, tanggalMasuk)
            self.tanggalMasukDateEdit.setDate(tglMasukDate)

        except Exception as e:
            # Menangkap kesalahan dan mencetak pesan
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def clear_inputs(self):
        self.kodeKaryawanLineEdit.clear()
        self.kodeKaryawanLineEdit.setEnabled(True)
        self.nIKLineEdit.clear()
        self.namaKaryawanLineEdit.clear()
        self.lakiRadio.setChecked(False)
        self.perempuanRadio.setChecked(False)
        self.agamaLineEdit.clear()
        self.alamatLineEdit.clear()
        self.noTelponLineEdit.clear()
        self.tempatLahirLineEdit.clear()
        self.tanggalLahirDateEdit.clear()
        self.statusKawinComboBox.setCurrentText("Belum Menikah")
        self.tanggalMasukDateEdit.clear()

    def add_data(self):
        kdKaryawan = self.kodeKaryawanLineEdit.text()
        nik = self.nIKLineEdit.text()
        namaKaryawan = self.namaKaryawanLineEdit.text()
        kdBagian = self.kodeBagianComboBox.currentText().split("/")[0]
        if self.jenisKelamin.checkedButton() :
            jenisKelamin = self.jenisKelamin.checkedButton().text()
        else :
            jenisKelamin = ""

        agama = self.agamaLineEdit.text()
        alamat = self.alamatLineEdit.text()
        noTelp = self.noTelponLineEdit.text()
        tempatLahir = self.tempatLahirLineEdit.text()
        tanggalLahir = self.tanggalLahirDateEdit.date().toString("yyyy-MM-dd")
        statusKawin = self.statusKawinComboBox.currentText()
        tanggalMasuk = self.tanggalMasukDateEdit.date().toString("yyyy-MM-dd")

        if kdKaryawan and nik and namaKaryawan and kdBagian and jenisKelamin and agama and alamat and noTelp and tempatLahir and tanggalLahir and statusKawin and tanggalMasuk:
            self.koneksiDB.tambah_karyawan(kdKaryawan, nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk)
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan.")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def update_data(self):

        kdKaryawan = self.kodeKaryawanLineEdit.text()
        nik = self.nIKLineEdit.text()
        namaKaryawan = self.namaKaryawanLineEdit.text()
        kdBagian = self.kodeBagianComboBox.currentText().split("/")[0]
        if self.jenisKelamin.checkedButton():
            jenisKelamin = self.jenisKelamin.checkedButton().text()
        else:
            jenisKelamin = ""

        agama = self.agamaLineEdit.text()
        alamat = self.alamatLineEdit.text()
        noTelp = self.noTelponLineEdit.text()
        tempatLahir = self.tempatLahirLineEdit.text()
        tanggalLahir = self.tanggalLahirDateEdit.date().toString("yyyy-MM-dd")
        statusKawin = self.statusKawinComboBox.currentText()
        tanggalMasuk = self.tanggalMasukDateEdit.date().toString("yyyy-MM-dd")

        if kdKaryawan and nik and namaKaryawan and kdBagian and jenisKelamin and agama and alamat and noTelp and tempatLahir and tanggalLahir and statusKawin and tanggalMasuk:
            try:
                # Ubah data di database
                self.koneksiDB.ubah_karyawan(kdKaryawan, nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.clear_inputs()
                self.load_data()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        kd_karyawan = self.kodeKaryawanLineEdit.text()
        self.koneksiDB.hapus_karyawan(kd_karyawan)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
        self.load_data()
        self.clear_inputs()

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("karyawan")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "karyawan_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=landscape(legal))
            width, height = landscape(legal)

            # Judul
            c.drawString((width/2)-50, height - 50, "Laporan Data Karyawan")

            # Set font and size
            c.setFont("Helvetica", 9)

            # Header tabel
            headers = ["KD Karyawan", "NIK", "Nama", "KD Bagian", "Jenis Kelamin", "Agama", "Alamat", "No Telpon", "Tempat Lahir", "Tanggal Lahir", "Status Kawin", "Tgl Masuk"]
            x_positions = [10, 90, 170, 250, 330, 410, 490, 570, 650, 730, 810, 890]
            row_height = 20

            # Draw header row
            y_position = height - 100
            for i, header in enumerate(headers):
                c.drawString(x_positions[i], y_position, header)
                c.rect(x_positions[i] - 5, y_position - 5, 80, row_height)  # Draw border

            # Menampilkan data

            y_position -= row_height
            for row in data:
                for i, cell in enumerate(row):
                    if isinstance(cell, date):
                        cell = cell.strftime("%Y-%m-%d")
                    c.drawString(x_positions[i], y_position, str(cell))
                    c.rect(x_positions[i] - 5, y_position - 5, 80, row_height)  # Draw border
                y_position -= row_height  # Move to next row

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")