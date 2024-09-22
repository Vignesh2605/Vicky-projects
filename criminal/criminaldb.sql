-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 13, 2024 at 01:24 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `criminaldb`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `uname` varchar(10) NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--


-- --------------------------------------------------------

--
-- Table structure for table `criminal`
--

CREATE TABLE `criminal` (
  `id` int(50) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `age` varchar(100) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `ctype` varchar(1000) NOT NULL,
  `image` varchar(1000) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `criminal`
--

INSERT INTO `criminal` (`id`, `name`, `age`, `address`, `ctype`, `image`) VALUES
(1, 'admin', '24', 'trichy', 'crime', 't3.jpg'),
(2, 'sundarpandiyan', '30', 'trichy', 'ssssss', 'sundar.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `criminalstatus`
--

CREATE TABLE `criminalstatus` (
  `id` int(10) NOT NULL auto_increment,
  `name` varchar(50) NOT NULL,
  `address` varchar(100) NOT NULL,
  `details` varchar(100) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `criminalstatus`
--

INSERT INTO `criminalstatus` (`id`, `name`, `address`, `details`) VALUES
(1, 'sundar', 'trichy', 'sharpening knives');

-- --------------------------------------------------------

--
-- Table structure for table `police`
--

CREATE TABLE `police` (
  `id` int(50) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL,
  `gender` varchar(100) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `sname` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  `post` varchar(100) NOT NULL,
  `details` varchar(100) NOT NULL,
  `Image` varchar(100) NOT NULL,
  `uname` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `police`
--

INSERT INTO `police` (`id`, `name`, `gender`, `phone`, `sname`, `location`, `post`, `details`, `Image`, `uname`, `password`) VALUES
(1, 'sundarpandiyan', 'male', '7904461600', 'sampletest', 'trichy', 's', 'sss', 't3.jpg', 'sss', 'sss');
