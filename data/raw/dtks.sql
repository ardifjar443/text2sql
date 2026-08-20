-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 29 Jul 2026 pada 16.58
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dtks`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `anggota_keluarga`
--

CREATE TABLE `anggota_keluarga` (
  `idsemesta` varchar(100) NOT NULL,
  `id_keluarga` varchar(100) DEFAULT NULL,
  `no_kk` varchar(30) DEFAULT NULL,
  `nik` varchar(30) DEFAULT NULL,
  `nama` varchar(200) DEFAULT NULL,
  `hub_kepala_keluarga` varchar(50) DEFAULT NULL,
  `pekerjaan_utama` varchar(150) DEFAULT NULL,
  `status_kedudukan_pekerjaan_utama` varchar(100) DEFAULT NULL,
  `id_deleted` varchar(5) DEFAULT NULL,
  `alasan_tolak_meninggal` varchar(255) DEFAULT NULL,
  `status_meninggal` varchar(5) DEFAULT NULL,
  `status_button_hamil` varchar(20) DEFAULT NULL,
  `keberadaan_anggota` varchar(100) DEFAULT NULL,
  `flag_aktif` int(11) DEFAULT NULL,
  `status_kpd` varchar(20) DEFAULT NULL,
  `button_status_ortu` varchar(20) DEFAULT NULL,
  `button_status_dapodik` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `aset_keluarga`
--

CREATE TABLE `aset_keluarga` (
  `id` int(11) NOT NULL,
  `id_keluarga` varchar(100) DEFAULT NULL,
  `id_jenis_aset` int(11) DEFAULT NULL,
  `jenis_aset` varchar(200) DEFAULT NULL,
  `jumlah` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `jenis_aset`
--

CREATE TABLE `jenis_aset` (
  `id_jenis_aset` int(11) NOT NULL,
  `jenis_aset` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `kabupaten`
--

CREATE TABLE `kabupaten` (
  `no_kab` varchar(5) NOT NULL,
  `no_prop` varchar(5) NOT NULL,
  `nama_kabupaten` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `kecamatan`
--

CREATE TABLE `kecamatan` (
  `no_kec` varchar(5) NOT NULL,
  `no_kab` varchar(5) NOT NULL,
  `no_prop` varchar(5) NOT NULL,
  `nama_kecamatan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `keluarga`
--

CREATE TABLE `keluarga` (
  `id_keluarga` varchar(100) NOT NULL,
  `no_kk` varchar(30) DEFAULT NULL,
  `nama_kepala_keluarga` varchar(200) DEFAULT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `desil_nasional` varchar(5) DEFAULT NULL,
  `peringkat_nasional` varchar(20) DEFAULT NULL,
  `id_wilayah` varchar(20) DEFAULT NULL,
  `padan_bulan_ini` int(11) DEFAULT NULL,
  `status_nonaktif` varchar(10) DEFAULT NULL,
  `no_prop` varchar(5) DEFAULT NULL,
  `no_kab` varchar(5) DEFAULT NULL,
  `no_kec` varchar(5) DEFAULT NULL,
  `no_kel` varchar(5) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `kelurahan`
--

CREATE TABLE `kelurahan` (
  `no_kel` varchar(5) NOT NULL,
  `no_kec` varchar(5) NOT NULL,
  `no_kab` varchar(5) NOT NULL,
  `no_prop` varchar(5) NOT NULL,
  `nama_kelurahan` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `provinsi`
--

CREATE TABLE `provinsi` (
  `no_prop` varchar(5) NOT NULL,
  `nama_propinsi` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_bpnt`
--

CREATE TABLE `riwayat_bpnt` (
  `id` int(11) NOT NULL,
  `id_keluarga` varchar(100) DEFAULT NULL,
  `nomor_kartu` varchar(50) DEFAULT NULL,
  `jenis_bantuan` varchar(50) DEFAULT NULL,
  `nama_periode` varchar(100) DEFAULT NULL,
  `nomor_rekening` varchar(50) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `nominal_bansos` varchar(30) DEFAULT NULL,
  `status_transaksi` varchar(255) DEFAULT NULL,
  `nama_penyalur` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_desil`
--

CREATE TABLE `riwayat_desil` (
  `id` int(11) NOT NULL,
  `id_keluarga` varchar(100) DEFAULT NULL,
  `desil` varchar(5) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_pbi`
--

CREATE TABLE `riwayat_pbi` (
  `id` int(11) NOT NULL,
  `idsemesta` varchar(100) DEFAULT NULL,
  `nik` varchar(30) DEFAULT NULL,
  `nama` varchar(200) DEFAULT NULL,
  `periode_awal` varchar(100) DEFAULT NULL,
  `status_awal` varchar(200) DEFAULT NULL,
  `periode_akhir` varchar(100) DEFAULT NULL,
  `status_akhir` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_pkh`
--

CREATE TABLE `riwayat_pkh` (
  `id` int(11) NOT NULL,
  `id_keluarga` varchar(100) DEFAULT NULL,
  `id_periode` varchar(50) DEFAULT NULL,
  `nomor_kartu` varchar(50) DEFAULT NULL,
  `jenis_bantuan` varchar(50) DEFAULT NULL,
  `nama_periode` varchar(100) DEFAULT NULL,
  `nomor_rekening` varchar(50) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `nominal_bansos` varchar(30) DEFAULT NULL,
  `status_transaksi` varchar(255) DEFAULT NULL,
  `nama_penyalur` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `anggota_keluarga`
--
ALTER TABLE `anggota_keluarga`
  ADD PRIMARY KEY (`idsemesta`),
  ADD KEY `id_keluarga` (`id_keluarga`);

--
-- Indeks untuk tabel `aset_keluarga`
--
ALTER TABLE `aset_keluarga`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_keluarga` (`id_keluarga`),
  ADD KEY `fk_aset_jenis` (`id_jenis_aset`);

--
-- Indeks untuk tabel `jenis_aset`
--
ALTER TABLE `jenis_aset`
  ADD PRIMARY KEY (`id_jenis_aset`);

--
-- Indeks untuk tabel `kabupaten`
--
ALTER TABLE `kabupaten`
  ADD PRIMARY KEY (`no_kab`,`no_prop`),
  ADD KEY `no_prop` (`no_prop`);

--
-- Indeks untuk tabel `kecamatan`
--
ALTER TABLE `kecamatan`
  ADD PRIMARY KEY (`no_kec`,`no_kab`,`no_prop`),
  ADD KEY `no_kab` (`no_kab`,`no_prop`);

--
-- Indeks untuk tabel `keluarga`
--
ALTER TABLE `keluarga`
  ADD PRIMARY KEY (`id_keluarga`),
  ADD KEY `no_kel` (`no_kel`,`no_kec`,`no_kab`,`no_prop`);

--
-- Indeks untuk tabel `kelurahan`
--
ALTER TABLE `kelurahan`
  ADD PRIMARY KEY (`no_kel`,`no_kec`,`no_kab`,`no_prop`),
  ADD KEY `no_kec` (`no_kec`,`no_kab`,`no_prop`);

--
-- Indeks untuk tabel `provinsi`
--
ALTER TABLE `provinsi`
  ADD PRIMARY KEY (`no_prop`);

--
-- Indeks untuk tabel `riwayat_bpnt`
--
ALTER TABLE `riwayat_bpnt`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_keluarga` (`id_keluarga`);

--
-- Indeks untuk tabel `riwayat_desil`
--
ALTER TABLE `riwayat_desil`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_keluarga` (`id_keluarga`);

--
-- Indeks untuk tabel `riwayat_pbi`
--
ALTER TABLE `riwayat_pbi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idsemesta` (`idsemesta`);

--
-- Indeks untuk tabel `riwayat_pkh`
--
ALTER TABLE `riwayat_pkh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_keluarga` (`id_keluarga`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `aset_keluarga`
--
ALTER TABLE `aset_keluarga`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `riwayat_bpnt`
--
ALTER TABLE `riwayat_bpnt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `riwayat_desil`
--
ALTER TABLE `riwayat_desil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `riwayat_pbi`
--
ALTER TABLE `riwayat_pbi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `riwayat_pkh`
--
ALTER TABLE `riwayat_pkh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `anggota_keluarga`
--
ALTER TABLE `anggota_keluarga`
  ADD CONSTRAINT `anggota_keluarga_ibfk_1` FOREIGN KEY (`id_keluarga`) REFERENCES `keluarga` (`id_keluarga`);

--
-- Ketidakleluasaan untuk tabel `aset_keluarga`
--
ALTER TABLE `aset_keluarga`
  ADD CONSTRAINT `aset_keluarga_ibfk_1` FOREIGN KEY (`id_keluarga`) REFERENCES `keluarga` (`id_keluarga`),
  ADD CONSTRAINT `fk_aset_jenis` FOREIGN KEY (`id_jenis_aset`) REFERENCES `jenis_aset` (`id_jenis_aset`) ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `kabupaten`
--
ALTER TABLE `kabupaten`
  ADD CONSTRAINT `kabupaten_ibfk_1` FOREIGN KEY (`no_prop`) REFERENCES `provinsi` (`no_prop`);

--
-- Ketidakleluasaan untuk tabel `kecamatan`
--
ALTER TABLE `kecamatan`
  ADD CONSTRAINT `kecamatan_ibfk_1` FOREIGN KEY (`no_kab`,`no_prop`) REFERENCES `kabupaten` (`no_kab`, `no_prop`);

--
-- Ketidakleluasaan untuk tabel `keluarga`
--
ALTER TABLE `keluarga`
  ADD CONSTRAINT `keluarga_ibfk_1` FOREIGN KEY (`no_kel`,`no_kec`,`no_kab`,`no_prop`) REFERENCES `kelurahan` (`no_kel`, `no_kec`, `no_kab`, `no_prop`);

--
-- Ketidakleluasaan untuk tabel `kelurahan`
--
ALTER TABLE `kelurahan`
  ADD CONSTRAINT `kelurahan_ibfk_1` FOREIGN KEY (`no_kec`,`no_kab`,`no_prop`) REFERENCES `kecamatan` (`no_kec`, `no_kab`, `no_prop`);

--
-- Ketidakleluasaan untuk tabel `riwayat_bpnt`
--
ALTER TABLE `riwayat_bpnt`
  ADD CONSTRAINT `riwayat_bpnt_ibfk_1` FOREIGN KEY (`id_keluarga`) REFERENCES `keluarga` (`id_keluarga`);

--
-- Ketidakleluasaan untuk tabel `riwayat_desil`
--
ALTER TABLE `riwayat_desil`
  ADD CONSTRAINT `riwayat_desil_ibfk_1` FOREIGN KEY (`id_keluarga`) REFERENCES `keluarga` (`id_keluarga`);

--
-- Ketidakleluasaan untuk tabel `riwayat_pbi`
--
ALTER TABLE `riwayat_pbi`
  ADD CONSTRAINT `riwayat_pbi_ibfk_1` FOREIGN KEY (`idsemesta`) REFERENCES `anggota_keluarga` (`idsemesta`);

--
-- Ketidakleluasaan untuk tabel `riwayat_pkh`
--
ALTER TABLE `riwayat_pkh`
  ADD CONSTRAINT `riwayat_pkh_ibfk_1` FOREIGN KEY (`id_keluarga`) REFERENCES `keluarga` (`id_keluarga`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
