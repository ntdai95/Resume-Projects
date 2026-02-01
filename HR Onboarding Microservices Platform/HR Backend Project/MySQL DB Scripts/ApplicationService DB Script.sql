-- CREATING DATABASE

CREATE DATABASE IF NOT EXISTS ApplicationService;
USE ApplicationService;

-- CREATING TABLES

DROP TABLE IF EXISTS ApplicationWorkFlow;
DROP TABLE IF EXISTS DigitalDocument;

CREATE TABLE IF NOT EXISTS ApplicationWorkFlow (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID VARCHAR(50),
    CreateDate DATE,
    LastModificationDate DATE,
    Status VARCHAR(50),
    Comment VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS DigitalDocument (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(50),
    isRequired BOOLEAN,
    Path VARCHAR(50),
    Description VARCHAR(100),
    Title VARCHAR(50)
);