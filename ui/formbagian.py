from PyQt6.QtWidgets import QWidget, QMessageBox
from PyQt6 import uic
from db.koneksi import KoneksiDB
from Model.TableModel import TableModel
# LIBRARY PDF
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class formBagian(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("formbagian.ui", self)
        # Instance DatabaseManager
        self.koneksiDB = KoneksiDB()
        data, headers = KoneksiDB().fetch_all("bagian")
        self.model = TableModel(data, headers)
        self.tableBagian.setModel(self.model)

        # menyambungkan fungsi ke tombol
        self.btnSimpan.clicked.connect(self.add_data)
        self.tableBagian.clicked.connect(self.on_table_click)
        self.btnUbah.clicked.connect(self.update_data)
        self.btnHapus.clicked.connect(self.delete_data)
        self.btnCetak.clicked.connect(self.print_pdf)

    def load_data(self):
        try:
            data, headers = KoneksiDB().fetch_all("bagian")
            self.model = TableModel(data, headers)
            self.tableBagian.setModel(self.model)
            # Pastikan 'table_view' adalah object name dari QTableView di Qt Designer
        except Exception as e:
            print(f"Terjadi kesalahan saat memuat data: {e}")

    def clear_inputs(self):
        self.kodeBagianLineEdit.clear()
        self.kodeBagianLineEdit.setEnabled(True)
        self.namaBagianLineEdit.clear()
        self.gajiPokokLineEdit.clear()
        self.uangTransportLineEdit.clear()
        self.uangMakanLineEdit.clear()
        self.uangLemburLineEdit.clear()

    def add_data(self):
        kdBagian = self.kodeBagianLineEdit.text()
        nmBagian = self.namaBagianLineEdit.text()
        gajiPokok = self.gajiPokokLineEdit.text()
        uangTransport = self.uangTransportLineEdit.text()
        uangMakan = self.uangMakanLineEdit.text()
        uangLembur = self.uangLemburLineEdit.text()

        if kdBagian and nmBagian and gajiPokok and uangTransport and uangMakan and uangLembur:
            self.koneksiDB.tambah_bagian(kdBagian, nmBagian, gajiPokok, uangTransport, uangMakan, uangLembur)
            QMessageBox.information(self, "Sukses", "Data berhasil disimpan.")
            self.clear_inputs()
            self.load_data()
        else:
            QMessageBox.warning(self, "Input Error", "Semua input harus diisi")

    def on_table_click(self, index):
        # Mendapatkan indeks baris yang diklik
        try:
            # Mendapatkan indeks baris yang diklik
            row = index.row()  # Mengambil nomor baris yang diklik
            column = index.column()  # Mengambil nomor kolom yang diklik

            # Ambil data dari model berdasarkan indeks
            record = self.model._data[row]

            # Ambil nilai dari kolom yang relevan
            kdBagian_value = str(record[0])
            nmBagian_value = str(record[1])
            gajiPokok_value = str(record[2])
            uangTransport_value = str(record[3])
            uangMakan_value = str(record[4])
            uangLembur_value = str(record[5])

            # print(f"Baris {row} diklik: NPM={npm_value}, Nama={nama_value}, Kelas={kelas_value}")

            self.kodeBagianLineEdit.setText(kdBagian_value)
            self.kodeBagianLineEdit.setEnabled(False)
            self.namaBagianLineEdit.setText(nmBagian_value)
            self.gajiPokokLineEdit.setText(gajiPokok_value)
            self.uangTransportLineEdit.setText(uangTransport_value)
            self.uangMakanLineEdit.setText(uangMakan_value)
            self.uangLemburLineEdit.setText(uangLembur_value)

        except Exception as e:
            # Menangkap kesalahan dan mencetak pesan
            print(f"Kesalahan saat memproses klik: {e}")
            QMessageBox.warning(self, "Error", f"Terjadi kesalahan: {e}")

    def update_data(self):

        kdBagian = self.kodeBagianLineEdit.text()
        nmBagian = self.namaBagianLineEdit.text()
        gajiPokok = self.gajiPokokLineEdit.text()
        uangTransport = self.uangTransportLineEdit.text()
        uangMakan = self.uangMakanLineEdit.text()
        uangLembur = self.uangLemburLineEdit.text()

        if kdBagian and nmBagian and gajiPokok and uangTransport and uangMakan and uangLembur:
            try:
                # Ubah data di database
                KoneksiDB().ubah_bagian(kdBagian, nmBagian, gajiPokok, uangTransport, uangMakan, uangLembur)
                QMessageBox.information(self, "Sukses", "Data berhasil diubah.")
                self.load_data()  # Reload data setelah mengubah
                self.clear_inputs()  # Kosongkan input setelah sukses
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Kesalahan saat mengubah data: {e}")
        else:
            QMessageBox.warning(self, "Peringatan", "Semua data harus diisi dan baris harus dipilih.")

    def delete_data(self):
        kd_bagian = self.kodeBagianLineEdit.text()
        self.koneksiDB.hapus_bagian(kd_bagian)
        QMessageBox.information(self, "Sukses", "Data berhasil dihapus.")
        self.load_data()
        self.clear_inputs()

    def print_pdf(self):
        try:
            data = self.koneksiDB.fetch_allPDF("bagian")
            if not data:
                QMessageBox.warning(self, "Data Kosong", "Tidak ada data untuk dicetak.")
                return

            pdf_file = "bagian_report.pdf"
            c = canvas.Canvas(pdf_file, pagesize=letter)
            width, height = letter

            # Judul
            c.drawString((width/2)-50, height - 50, "Laporan Data Bagian")

            # Header tabel
            headers = ["Kode Bagian", "Nama Bagian", "Gaji Pokok", "Uang Transport", "Uang Makan", "Uang Lembur"]
            x_positions = [10, 110, 210, 310, 410, 510]
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
                    c.drawString(x_positions[i], y_position, str(cell))
                    c.rect(x_positions[i] - 5, y_position - 5, 100, row_height)  # Draw border
                y_position -= row_height  # Move to next row

            c.save()
            QMessageBox.information(self, "Sukses", f"Laporan telah dicetak ke {pdf_file}")

        except Exception as e:
            QMessageBox.critical(self, "Kesalahan", f"Terjadi kesalahan saat mencetak PDF: {e}")
