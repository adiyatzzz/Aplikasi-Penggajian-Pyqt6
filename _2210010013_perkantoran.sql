-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 08, 2025 at 02:37 AM
-- Server version: 8.0.30
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `_2210010013_perkantoran`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi`
--

CREATE TABLE `absensi` (
  `id_absen` varchar(20) NOT NULL,
  `kd_karyawan` varchar(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jam_masuk` time DEFAULT NULL,
  `jam_keluar` time DEFAULT NULL,
  `status_kehadiran` varchar(20) NOT NULL,
  `jenis_kerja` varchar(20) NOT NULL,
  `keterangan` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `absensi`
--

INSERT INTO `absensi` (`id_absen`, `kd_karyawan`, `tanggal`, `jam_masuk`, `jam_keluar`, `status_kehadiran`, `jenis_kerja`, `keterangan`) VALUES
('ABS-001', 'KRY-001', '2024-12-19', '08:49:10', '18:49:10', 'Hadir', 'On Site', 'tidak ada'),
('ABS-002', 'KRY-002', '2024-12-17', '10:00:00', '20:00:00', 'Hadir', 'WFH', 'Tidak ada');

-- --------------------------------------------------------

--
-- Table structure for table `bagian`
--

CREATE TABLE `bagian` (
  `kd_bagian` varchar(11) NOT NULL,
  `nm_bagian` varchar(20) NOT NULL,
  `gaji_pokok` decimal(20,0) NOT NULL,
  `uang_transport` decimal(20,0) NOT NULL,
  `uang_makan` decimal(20,0) NOT NULL,
  `uang_lembur` decimal(20,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bagian`
--

INSERT INTO `bagian` (`kd_bagian`, `nm_bagian`, `gaji_pokok`, `uang_transport`, `uang_makan`, `uang_lembur`) VALUES
('BGN-001', 'Gudang Barang', '3500000', '500000', '300000', '50000'),
('BGN-002', 'HRD', '10000000', '500000', '600000', '80000'),
('BGN-003', 'Admin', '3000000', '300000', '2000000', '1000000');

-- --------------------------------------------------------

--
-- Table structure for table `karyawan`
--

CREATE TABLE `karyawan` (
  `kd_karyawan` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `nik` varchar(20) NOT NULL,
  `nm_karyawan` varchar(50) NOT NULL,
  `kd_bagian` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `kelamin` varchar(20) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `agama` varchar(20) NOT NULL,
  `alamat_tinggal` text NOT NULL,
  `no_telepon` varchar(20) NOT NULL,
  `tempat_lahir` varchar(50) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL,
  `tanggal_lahir` date NOT NULL,
  `status_kawin` varchar(20) NOT NULL,
  `tanggal_masuk` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `karyawan`
--

INSERT INTO `karyawan` (`kd_karyawan`, `nik`, `nm_karyawan`, `kd_bagian`, `kelamin`, `agama`, `alamat_tinggal`, `no_telepon`, `tempat_lahir`, `tanggal_lahir`, `status_kawin`, `tanggal_masuk`) VALUES
('KRY-001', '6472819340219421', 'Udin Knalpot', 'BGN-001', 'Laki - Laki', 'Islam', 'Jl. Sutoyo S No. 155', '098724812742', 'Banjarmasin', '1995-12-12', 'Belum Menikah', '2024-12-03'),
('KRY-002', '1122233', 'Ayu Wati', 'BGN-002', 'Perempuan', 'Katolik', 'Jl. Cemara Ujung', '7895655533', 'Martapura', '1977-02-12', 'Sudah Menikah', '2000-10-19');

-- --------------------------------------------------------

--
-- Table structure for table `lembur`
--

CREATE TABLE `lembur` (
  `id` varchar(20) NOT NULL,
  `kd_karyawan` varchar(11) NOT NULL,
  `tanggal` date NOT NULL,
  `keterangan` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `lembur`
--

INSERT INTO `lembur` (`id`, `kd_karyawan`, `tanggal`, `keterangan`) VALUES
('LBR-001', 'KRY-001', '2024-12-27', 'Angkut Barang'),
('LBR-002', 'KRY-002', '2024-12-30', 'Lembur nataru');

-- --------------------------------------------------------

--
-- Table structure for table `penggajian`
--

CREATE TABLE `penggajian` (
  `no_penggajian` varchar(11) NOT NULL,
  `periode_gaji` varchar(11) NOT NULL,
  `tanggal` date NOT NULL,
  `kd_karyawan` varchar(11) NOT NULL,
  `gaji_pokok` decimal(10,0) NOT NULL,
  `tunj_transport` decimal(10,0) NOT NULL,
  `tunj_makan` decimal(10,0) NOT NULL,
  `total_lembur` decimal(10,0) NOT NULL,
  `total_bonus` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `penggajian`
--

INSERT INTO `penggajian` (`no_penggajian`, `periode_gaji`, `tanggal`, `kd_karyawan`, `gaji_pokok`, `tunj_transport`, `tunj_makan`, `total_lembur`, `total_bonus`) VALUES
('GJI-001', 'DES24', '2024-12-31', 'KRY-001', '3500000', '500000', '300000', '50000', '200000'),
('GJI-002', 'DES24', '2024-12-31', 'KRY-002', '10000000', '500000', '600000', '200000', '100000');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi`
--
ALTER TABLE `absensi`
  ADD PRIMARY KEY (`id_absen`),
  ADD KEY `kd_karyawan` (`kd_karyawan`);

--
-- Indexes for table `bagian`
--
ALTER TABLE `bagian`
  ADD PRIMARY KEY (`kd_bagian`);

--
-- Indexes for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD PRIMARY KEY (`kd_karyawan`),
  ADD KEY `kd_bagian` (`kd_bagian`);

--
-- Indexes for table `lembur`
--
ALTER TABLE `lembur`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kd_karyawan` (`kd_karyawan`);

--
-- Indexes for table `penggajian`
--
ALTER TABLE `penggajian`
  ADD PRIMARY KEY (`no_penggajian`),
  ADD KEY `kd_karyawan` (`kd_karyawan`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi`
--
ALTER TABLE `absensi`
  ADD CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`kd_karyawan`) REFERENCES `karyawan` (`kd_karyawan`);

--
-- Constraints for table `karyawan`
--
ALTER TABLE `karyawan`
  ADD CONSTRAINT `karyawan_ibfk_1` FOREIGN KEY (`kd_bagian`) REFERENCES `bagian` (`kd_bagian`);

--
-- Constraints for table `lembur`
--
ALTER TABLE `lembur`
  ADD CONSTRAINT `lembur_ibfk_1` FOREIGN KEY (`kd_karyawan`) REFERENCES `karyawan` (`kd_karyawan`);

--
-- Constraints for table `penggajian`
--
ALTER TABLE `penggajian`
  ADD CONSTRAINT `penggajian_ibfk_1` FOREIGN KEY (`kd_karyawan`) REFERENCES `karyawan` (`kd_karyawan`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
