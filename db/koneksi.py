
import pymysql
from mysql.connector import Error
from decimal import Decimal

class KoneksiDB:
    def __init__(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                user='root',  # Ganti dengan username MySQL Anda
                password='',  # Ganti dengan password MySQL Anda
                database='_2210010013_perkantoran'  # Ganti dengan nama database Anda
            )

            # Memastikan koneksi berhasil
            if self.connection.open:
                print("Koneksi berhasil")
                self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Terjadi kesalahan: {e}")

    def fetch_all(self, tableName):
        self.cursor.execute(f"SELECT * FROM {tableName}")
        data = self.cursor.fetchall()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def fetch_allPDF(self, tableName):
        try:
            self.cursor.execute(f"SELECT * FROM {tableName}")
            results = self.cursor.fetchall()
            print("Results fetched:", results)  # Tambahkan ini untuk debugging
            return results
        except pymysql.connector.Error as err:
            print(f"Kesalahan saat mengambil data: {err}")
            return []

    # method table bagian
    def tambah_bagian(self, kd_bagian, nm_bagian, gaji_pokok, uang_transport, uang_makan, uang_lembur):
        self.cursor.execute("INSERT INTO bagian (kd_bagian, nm_bagian, gaji_pokok, uang_transport, uang_makan, uang_lembur) VALUES (%s, %s, %s, %s, %s, %s)", (kd_bagian, nm_bagian, gaji_pokok, uang_transport, uang_makan, uang_lembur))
        self.connection.commit()

    def ubah_bagian(self, kd_bagian, nm_bagian, gaji_pokok, uang_transport, uang_makan, uang_lembur):
        self.cursor.execute("UPDATE bagian SET nm_bagian = %s, gaji_pokok = %s, uang_transport = %s, uang_makan = %s, uang_lembur = %s WHERE kd_bagian = %s",(nm_bagian, gaji_pokok, uang_transport, uang_makan, uang_lembur, kd_bagian))
        self.connection.commit()

    def hapus_bagian(self, kd_bagian):
        self.cursor.execute("DELETE FROM bagian WHERE kd_bagian = %s", (kd_bagian))
        self.connection.commit()
    # end method table bagian

    # method table karyawan
    def tambah_karyawan(self, kdKaryawan, nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk):
        self.cursor.execute("INSERT INTO karyawan (kd_karyawan, nik, nm_karyawan, kd_bagian, kelamin, agama, alamat_tinggal, no_telepon, tempat_lahir, tanggal_lahir, status_kawin, tanggal_masuk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (kdKaryawan, nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk))
        self.connection.commit()

    def ubah_karyawan(self, kdKaryawan, nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk):
        self.cursor.execute("UPDATE karyawan SET nik = %s, nm_karyawan = %s, kd_bagian = %s, kelamin = %s, agama = %s, alamat_tinggal = %s, no_telepon = %s, tempat_lahir = %s, tanggal_lahir = %s, status_kawin = %s, tanggal_masuk = %s WHERE kd_karyawan = %s",(nik, namaKaryawan, kdBagian, jenisKelamin, agama, alamat, noTelp, tempatLahir, tanggalLahir, statusKawin, tanggalMasuk, kdKaryawan))
        self.connection.commit()

    def hapus_karyawan(self, kdKaryawan):
        self.cursor.execute("DELETE FROM karyawan WHERE kd_karyawan = %s", (kdKaryawan))
        self.connection.commit()
    # end method table karyawan

    # method table absensi
    def tambah_absensi(self, idAbsensi, kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan):
        self.cursor.execute("INSERT INTO absensi (id_absen, kd_karyawan, tanggal, jam_masuk, jam_keluar, status_kehadiran, jenis_kerja, keterangan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (idAbsensi, kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan))
        self.connection.commit()

    def ubah_absensi(self, idAbsensi, kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan):
        self.cursor.execute("UPDATE absensi SET kd_karyawan = %s, tanggal = %s, jam_masuk = %s, jam_keluar = %s, status_kehadiran = %s, jenis_kerja = %s, keterangan = %s WHERE id_absen = %s",( kdKaryawan, tanggal, jamMasuk, jamKeluar, kehadiran, jenisKerja, keterangan, idAbsensi))
        self.connection.commit()

    def hapus_absensi(self, idAbsensi):
        self.cursor.execute("DELETE FROM absensi WHERE id_absen = %s", (idAbsensi))
        self.connection.commit()
    # end method table absensi

    # method table lembur
    def tambah_lembur(self, idLembur, kdKaryawan, tanggal, keterangan):
        self.cursor.execute("INSERT INTO lembur (id, kd_karyawan, tanggal, keterangan) VALUES (%s, %s, %s, %s)", (idLembur, kdKaryawan, tanggal, keterangan))
        self.connection.commit()

    def ubah_lembur(self, idLembur, kdKaryawan, tanggal, keterangan):
        self.cursor.execute("UPDATE lembur SET kd_karyawan = %s, tanggal = %s,  keterangan = %s WHERE id = %s",(kdKaryawan, tanggal, keterangan, idLembur))
        self.connection.commit()

    def hapus_lembur(self, idLembur):
        self.cursor.execute("DELETE FROM lembur WHERE id = %s", (idLembur))
        self.connection.commit()
    # end method table lembur

    # method penggajian
    def getGajiBagian(self, kdKaryawan):
        self.cursor.execute(f"SELECT bagian.*, karyawan.kd_karyawan, karyawan.nm_karyawan FROM karyawan INNER JOIN bagian ON bagian.kd_bagian = karyawan.kd_bagian WHERE karyawan.kd_karyawan = %s", kdKaryawan)
        data = self.cursor.fetchone()
        headers = [desc[0] for desc in self.cursor.description]
        return data, headers

    def tambah_penggajian(self, noPenggajian, periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus):
        self.cursor.execute("INSERT INTO penggajian (no_penggajian, periode_gaji, tanggal, kd_karyawan, gaji_pokok, tunj_transport, tunj_makan, total_lembur, total_bonus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (noPenggajian, periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus))
        self.connection.commit()

    def ubah_penggajian(self, noPenggajian, periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus):
        self.cursor.execute("UPDATE penggajian SET periode_gaji = %s, tanggal = %s,  kd_karyawan  = %s, gaji_pokok  = %s, tunj_transport  = %s, tunj_makan  = %s, total_lembur  = %s, total_bonus = %s WHERE no_penggajian  = %s",(periodeGaji, tanggal, kdKaryawan, gajiPokok, tunjTransportasi, tunjMakan, totalLembur, totalBonus, noPenggajian))
        self.connection.commit()

    def hapus_penggajian(self, noPenggajian):
        self.cursor.execute("DELETE FROM penggajian WHERE no_penggajian = %s", (noPenggajian))
        self.connection.commit()
    # end method penggajian

    def close(self):
        self.connection.close()


