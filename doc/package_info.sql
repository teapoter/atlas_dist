-- phpMyAdmin SQL Dump
-- version 3.5.2
-- http://www.phpmyadmin.net
--
-- 主机: 10.181.158.94:3988
-- 生成日期: 2014 年 10 月 22 日 17:29
-- 服务器版本: 5.1.54-CDB-3.0.4
-- PHP 版本: 5.3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES latin1 */;

--
-- 数据库: `host_mgr`
--

-- --------------------------------------------------------

--
-- 表的结构 `package_info`
--

CREATE TABLE IF NOT EXISTS `package_info` (
  `pkgName` varchar(128) NOT NULL COMMENT '包所在文件夹名称',
  `description` varchar(128) NOT NULL DEFAULT 'no info input' COMMENT '包描述',
  `fileServer` varchar(64) NOT NULL DEFAULT 'localhost' COMMENT '存储文件的服务器ip地址',
  `storePath` varchar(128) NOT NULL COMMENT '存储路径',
  `fileName` varchar(128) NOT NULL COMMENT '文件名称',
  `md5Info` varchar(64) NOT NULL COMMENT 'md5信息',
  `initMd5Info` varchar(64) NOT NULL COMMENT '录入的md5信息',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updateTime` datetime NOT NULL COMMENT '更新时间',
  `creator` varchar(32) NOT NULL COMMENT '创建人',
  `flag` tinyint(2) NOT NULL,
  PRIMARY KEY (`storePath`,`fileName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC COMMENT='存储上传的包信息';

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
