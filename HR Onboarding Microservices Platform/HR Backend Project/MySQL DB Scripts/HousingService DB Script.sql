-- CREATING DATABASE

CREATE DATABASE IF NOT EXISTS HousingService;
USE HousingService;

-- CREATING TABLES

DROP TABLE IF EXISTS FacilityReportDetail;
DROP TABLE IF EXISTS FacilityReport;
DROP TABLE IF EXISTS Facility;
DROP TABLE IF EXISTS House;
DROP TABLE IF EXISTS Landlord;

CREATE TABLE IF NOT EXISTS Landlord (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Email VARCHAR(50),
    CellPhone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS House (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    LandlordID INT,
    Address VARCHAR(100),
    MaxOccupant INT,
    FOREIGN KEY (LandlordID) REFERENCES Landlord(ID)
);

CREATE TABLE IF NOT EXISTS Facility (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    HouseID INT,
    Type VARCHAR(50),
    Description VARCHAR(100),
    Quantity INT,
    FOREIGN KEY (HouseID) REFERENCES House(ID)
);

CREATE TABLE IF NOT EXISTS FacilityReport (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    FacilityID INT,
    EmployeeID VARCHAR(50),
    Title VARCHAR(50),
    Description VARCHAR(100),
    CreateDate DATE,
    Status VARCHAR(50),
    FOREIGN KEY (FacilityID) REFERENCES Facility(ID)
);

CREATE TABLE IF NOT EXISTS FacilityReportDetail (
	ID INT AUTO_INCREMENT PRIMARY KEY,
    FacilityReportID INT,
    EmployeeID VARCHAR(50),
    Comment VARCHAR(100),
    CreateDate DATE,
    LastModificationDate DATE,
    FOREIGN KEY (FacilityReportID) REFERENCES FacilityReport(ID)
);

INSERT INTO Landlord (FirstName, LastName, Email, CellPhone) VALUES ("Emily", "Blunt", "eb@gmail.com", "64362");
INSERT INTO House (LandlordID, Address, MaxOccupant) VALUES (1, "2603 Tokyo Drive", 3);
INSERT INTO Facility (HouseID, Type, Description, Quantity) VALUES (1, "bed", "number of beds", 1);
INSERT INTO Facility (HouseID, Type, Description, Quantity) VALUES (1, "mattress", "number of mattresses", 2);
INSERT INTO Facility (HouseID, Type, Description, Quantity) VALUES (1, "table", "number of tables", 3);
INSERT INTO Facility (HouseID, Type, Description, Quantity) VALUES (1, "chair", "number of chairs", 4);
INSERT INTO FacilityReport (FacilityID, EmployeeID, Title, Description, CreateDate, Status) VALUES (1, "gfreigyr67", "Broken Bed", "The bed in the room has broken legs", "2022-08-16", "Open");
INSERT INTO FacilityReportDetail (FacilityReportID, EmployeeID, Comment, CreateDate, LastModificationDate) VALUES (1, "74638683Afu", "Issue still persist.", "2022-08-16", "2022-08-16");