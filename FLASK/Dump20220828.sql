-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: notemedia2
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `note_id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(50) DEFAULT NULL,
  `price` int DEFAULT NULL,
  `subject` varchar(20) DEFAULT NULL,
  `publisher_id` int DEFAULT NULL,
  `verified` tinyint(1) DEFAULT NULL,
  `description` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`note_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (1,'ray optics',49,'physics',1,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(2,'d and f block',49,'chemistry',2,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(3,'haloalkanes',49,'chemistry',2,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(4,'3d geometry',49,'maths',1,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(5,'metrices',39,'maths',2,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(6,'integrals',39,'maths',2,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(7,'current electricity',39,'physics',1,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(9,'aldehydes',45,'chemistry',1,0,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(10,'wave optics',45,'physics',1,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(11,'magnetism',45,'physics',1,0,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(12,'probability',45,'maths',1,0,'20 pages\n 50 board questions\n 60 jee questions\n 1 test'),(13,'diffretiation',45,'maths',1,1,'20 pages\n 50 board questions\n 60 jee questions\n 1 test');
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `publishers`
--

DROP TABLE IF EXISTS `publishers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `publishers` (
  `qualification` varchar(50) DEFAULT NULL,
  `about` varchar(200) DEFAULT NULL,
  `user_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `publishers`
--

LOCK TABLES `publishers` WRITE;
/*!40000 ALTER TABLE `publishers` DISABLE KEYS */;
INSERT INTO `publishers` VALUES ('iit mubai first rank','profettial level notes by air-1 rank holder in jee',1),('prof at harward','i make good notes padiku santhoshiku maryadaku padichal 100% guareteed',2);
/*!40000 ALTER TABLE `publishers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `purchases`
--

DROP TABLE IF EXISTS `purchases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `purchases` (
  `purchase_id` int DEFAULT NULL,
  `note_id` int DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `date_and_time` datetime DEFAULT NULL,
  `rating` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `purchases`
--

LOCK TABLES `purchases` WRITE;
/*!40000 ALTER TABLE `purchases` DISABLE KEYS */;
/*!40000 ALTER TABLE `purchases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'navadeepsatheesh@gmail.com','1234','navadeep satheesh'),(2,'ashvinpkumar2004@gmail.com','2345','ashvin p kumar');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `verifiers`
--

DROP TABLE IF EXISTS `verifiers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `verifiers` (
  `verifier_id` int DEFAULT NULL,
  `verifier_name` varchar(50) DEFAULT NULL,
  `verifier_email` varchar(50) DEFAULT NULL,
  `verifier_password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `verifiers`
--

LOCK TABLES `verifiers` WRITE;
/*!40000 ALTER TABLE `verifiers` DISABLE KEYS */;
INSERT INTO `verifiers` VALUES (1,'navadeep satheesh','navadeepsatheesh@gmail.com','1234'),(2,'ashvinpkumar','ashvinpkumar2004@gmail.com','1234'),(3,'samanya','samanya@gmail.com','2345');
/*!40000 ALTER TABLE `verifiers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-28 11:49:29
