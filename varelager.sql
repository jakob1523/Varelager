CREATE DATABASE varelager;

CREATE TABLE `varer` (
 `id` int NOT NULL AUTO_INCREMENT,
 `varenummer` varchar(50) NOT NULL,
 `navn` varchar(100) NOT NULL,
 `kategori` varchar(50) DEFAULT NULL,
 `antall` int NOT NULL,
 `pris` decimal(10,2) NOT NULL,
 PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci

CREATE TABLE `varelogg` (
 `id` int NOT NULL AUTO_INCREMENT,
 `varenummer` int NOT NULL,
 `endring` varchar(255) NOT NULL,
 `tidspunkt` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY (`id`),
 KEY `varenummer` (`varenummer`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci


Lage brukere:

Admin bruker:

CREATE USER 'varelager'@'localhost' IDENTIFIED BY '123';
GRANT ALL PRIVILEGES ON varelager.* TO 'varelager'@'localhost';
FLUSH PRIVILEGES;


Normal bruker for å se:

CREATE USER 'varese'@'localhost' IDENTIFIED BY '321';
GRANT SELECT ON varelager.* TO 'varese'@'localhost';
FLUSH PRIVILEGES;
