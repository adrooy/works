CREATE DATABASE  IF NOT EXISTS `sdcleaner` DEFAULT CHARACTER SET=utf8;
USE `sdcleaner`;

CREATE TABLE `apk_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `package_name` varchar(200) NOT NULL,
  `title` varchar(2000) NOT NULL,
  `assign_to` varchar(2000) NOT NULL,
  `assign_time` timestamp DEFAULT '0000-00-00 00:00:00',
  `last_modified` timestamp DEFAULT CURRENT_TIMESTAMP,
  `finished` tinyint(1) NOT NULL DEFAULT 0,
  `approved` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`package_name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `path_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_path` varchar(2000) NOT NULL,
  `item_name` varchar(2000) NOT NULL,
  `alert_info` varchar(2000) NOT NULL,
  `desc` varchar(2000) NOT NULL,
  `sub_path` varchar(2000) DEFAULT NULL,
  `sl` varchar(100) DEFAULT NULL,
  `apk_id` int NOT NULL,
  `path_hash` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique` (`path_hash`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
