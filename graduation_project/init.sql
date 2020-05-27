CREATE DATABASE IF NOT EXISTS diplom_db;
DROP USER IF EXISTS 'test_qa'@'%';
CREATE USER 'test_qa'@'%' IDENTIFIED BY 'qa_test';
GRANT ALL PRIVILEGES ON diplom_db.* to 'test_qa'@'%';
FLUSH PRIVILEGES ;
USE diplom_db;

CREATE TABLE IF NOT EXISTS `test_users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(16) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(64) NOT NULL,
  `access` smallint DEFAULT NULL,
  `active` smallint DEFAULT NULL,
  `start_active_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `ix_test_users_username` (`username`)
);