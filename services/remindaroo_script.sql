CREATE DATABASE IF NOT EXISTS `remindaroo_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
SHOW DATABASES;

USE `remindaroo_db`;

CREATE TABLE IF NOT EXISTS `r_user_details` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
  	`username` varchar(50) NOT NULL,
  	`password` varchar(255) NOT NULL,
  	`email` varchar(100) NOT NULL,
	`date` datetime NOT NULL,	
	`mobile` varchar(17) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `r_app_details` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`subject` varchar(255) NOT NULL,
	`description` text NOT NULL,
	`status` varchar(30) NOT NULL,
	PRIMARY KEY(`id`)	
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

ALTER TABLE remindaroo_db.r_user_details MODIFY id int(11) NOT NULL AUTO_INCREMENT;


SELECT * FROM `remindaroo_db`.`r_user_details` LIMIT 1000;
SELECT * FROM `remindaroo_db`.`r_app_details` LIMIT 1000;

INSERT INTO `remindaroo_db`.`r_user_details` (`id`, `username`, `password`, `email`,`date`,`mobile`) VALUES (2, 'test', 'test', 'test@test.com','2020-02-04 02:18','09999999999');

INSERT INTO `remindaroo_db`.`r_app_details` (`id`,`subject`,`description`,`status`) VALUES (2,'test subject', 'test description','True');

UPDATE `r_app_details` SET status="FALSE" WHERE rem_id='1581018984.032295';