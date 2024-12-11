
CREATE DATABASE padNotify;

USE padNotify;

CREATE TABLE `notify` (
   `id` int NOT NULL,
   `title` varchar(200) NOT NULL,
   `date` date DEFAULT NULL,
   `origin` varchar(1000) NOT NULL,
   PRIMARY KEY (`id`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `event` (
   `name` varchar(100) NOT NULL,
   `link` varchar(200) NOT NULL,
   `status` varchar(10) NOT NULL,
   `start_date` date DEFAULT NULL,
   `end_date` date DEFAULT NULL,
   `update_date` date DEFAULT NULL,
   PRIMARY KEY (`name`)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;