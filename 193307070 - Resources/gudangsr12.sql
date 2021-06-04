-- phpMyAdmin SQL Dump
-- version 4.2.11
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: May 20, 2021 at 05:55 AM
-- Server version: 5.6.21
-- PHP Version: 5.6.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `gudangsr12`
--

-- --------------------------------------------------------

--
-- Table structure for table `t_barang`
--

CREATE TABLE IF NOT EXISTS `t_barang` (
  `idBarang` int(11) NOT NULL DEFAULT '0',
  `namaBarang` varchar(250) NOT NULL,
  `kategori` varchar(25) NOT NULL,
  `harga` int(20) NOT NULL,
  `kuantitas` int(11) NOT NULL,
  `deskripsi` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `t_barang`
--

INSERT INTO `t_barang` (`idBarang`, `namaBarang`, `kategori`, `harga`, `kuantitas`, `deskripsi`) VALUES
(1, 'Salimah Slim', 'Healthy Care', 60000, 70, 'Netto 60 kapsul, dikonsumsi sejam setelah makan 3x sehari\n'),
(2, 'Lipcream', 'Face Care', 100000, 40, 'Netto 5g\n\n\n'),
(3, 'Sabun Kopi', 'Facial Wash', 22000, 47, 'Netto 22 gr\n');

-- --------------------------------------------------------

--
-- Table structure for table `t_pengiriman`
--

CREATE TABLE IF NOT EXISTS `t_pengiriman` (
  `idPengiriman` int(10) NOT NULL DEFAULT '0',
  `namaBarang` varchar(250) NOT NULL,
  `tglPengiriman` date NOT NULL,
  `tujuan` varchar(250) NOT NULL,
  `kuantitas` int(10) NOT NULL,
  `deskripsi` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `t_pengiriman`
--

INSERT INTO `t_pengiriman` (`idPengiriman`, `namaBarang`, `tglPengiriman`, `tujuan`, `kuantitas`, `deskripsi`) VALUES
(1, 'Salimah Slim', '2021-05-18', 'Bali', 30, 'mjcbxmbcmx\n'),
(2, 'Lipglow', '2021-05-04', 'Madiun', 5, 'Netto 2g\n'),
(3, 'Sabun Kopi', '2021-04-30', 'Surabaya', 3, 'xkncbkxncbk\n');

--
-- Triggers `t_pengiriman`
--
DELIMITER //
CREATE TRIGGER `deletekeluar` BEFORE DELETE ON `t_pengiriman`
 FOR EACH ROW UPDATE 
	t_barang SET t_barang.kuantitas = t_barang.kuantitas + OLD.kuantitas 
    WHERE t_barang.namaBarang = OLD.namaBarang
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER `keluar` BEFORE INSERT ON `t_pengiriman`
 FOR EACH ROW BEGIN
	UPDATE t_barang
    SET kuantitas = t_barang.kuantitas - NEW.kuantitas WHERE namaBarang = new.namaBarang;
END
//
DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `t_permintaan`
--

CREATE TABLE IF NOT EXISTS `t_permintaan` (
  `idPenerimaan` int(20) NOT NULL DEFAULT '0',
  `namaBarang` varchar(250) NOT NULL,
  `tglPenerimaan` date NOT NULL,
  `sumber` varchar(250) NOT NULL,
  `kuantitas` int(20) NOT NULL,
  `deskripsi` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `t_permintaan`
--

INSERT INTO `t_permintaan` (`idPenerimaan`, `namaBarang`, `tglPenerimaan`, `sumber`, `kuantitas`, `deskripsi`) VALUES
(1, 'Salimah Slim', '2010-05-21', 'Bogor', 100, 'Netto 60 kapsul\n'),
(2, 'Lipcare', '2021-05-01', 'Bogor', 50, 'Netto 5g\n'),
(3, 'Sabun Kopi', '2021-05-18', 'Bogor', 50, 'Netto 22 gr\n'),
(4, 'VCO Kapsul', '2021-05-20', 'Bali', 40, 'Netto 100 kapsul\n');

--
-- Triggers `t_permintaan`
--
DELIMITER //
CREATE TRIGGER `deletemasuk` BEFORE DELETE ON `t_permintaan`
 FOR EACH ROW UPDATE 
	t_barang SET t_barang.kuantitas = t_barang.kuantitas - OLD.kuantitas 
    WHERE t_barang.namaBarang = OLD.namaBarang
//
DELIMITER ;
DELIMITER //
CREATE TRIGGER `masuk` BEFORE INSERT ON `t_permintaan`
 FOR EACH ROW BEGIN
	UPDATE t_barang
    SET kuantitas = t_barang.kuantitas + NEW.kuantitas WHERE namaBarang = new.namaBarang;
END
//
DELIMITER ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `t_barang`
--
ALTER TABLE `t_barang`
 ADD PRIMARY KEY (`idBarang`), ADD UNIQUE KEY `idBarang` (`idBarang`);

--
-- Indexes for table `t_pengiriman`
--
ALTER TABLE `t_pengiriman`
 ADD PRIMARY KEY (`idPengiriman`);

--
-- Indexes for table `t_permintaan`
--
ALTER TABLE `t_permintaan`
 ADD PRIMARY KEY (`idPenerimaan`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
