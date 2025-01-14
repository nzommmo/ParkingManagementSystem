Create Database PackingManagementSystem;

Use PackingManagementSystem;

CREATE TABLE Users (
    UserId INT PRIMARY KEY AUTO_INCREMENT,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Role ENUM('Admin', 'Parking-lot Attendant', 'User') DEFAULT 'User',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE Pricing_Rates (
    Rate_id INT PRIMARY KEY AUTO_INCREMENT,
    Rate DECIMAL(10, 2) NOT NULL,
    Description TEXT
);

CREATE TABLE Tickets (
    TicketId INT PRIMARY KEY AUTO_INCREMENT,
    Assigned_TO VARCHAR(255) UNIQUE NOT NULL, -- Vehicle registration number
    UserId INT NULL,
    Guest_Email VARCHAR(255) NULL,
    Guest_Phone VARCHAR(15) NULL,
    Stay_Duration TIME AS (TIMEDIFF(End_Time, Start_Time)) STORED, -- Calculated Duration
    Start_Time DATETIME NOT NULL,
    End_Time DATETIME NULL, -- End Time will be updated when status changes to 'Payment_In_Progress'
    Rate_id INT NOT NULL,
    Status ENUM('Paid', 'Payment_In_Progress', 'Unpaid') DEFAULT 'Unpaid',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    FOREIGN KEY (Rate_id) REFERENCES Pricing_Rates(Rate_id)
);

CREATE TABLE Payments (
    PaymentId INT PRIMARY KEY AUTO_INCREMENT,
    TicketId INT NOT NULL,
    Amount DECIMAL(10, 2) DEFAULT 0, -- Default amount is 0
    Payment_Method ENUM('Mpesa', 'Cash', 'Bank') DEFAULT 'Cash', -- Default Payment Method is Cash
    Payment_Status ENUM('Pending', 'Completed') DEFAULT 'Pending',
    Payment_Date DATETIME NULL,
    Payment_Time DATETIME NULL,
    FOREIGN KEY (TicketId) REFERENCES Tickets(TicketId)
);

ALTER TABLE Tickets
    MODIFY Start_Time DATETIME DEFAULT CURRENT_TIMESTAMP;
    
    
ALTER TABLE Tickets
ADD CONSTRAINT chk_guest_contact
CHECK (
    (UserId IS NULL AND (Guest_Email IS NOT NULL AND Guest_Email <> '' OR Guest_Phone IS NOT NULL AND Guest_Phone <> '')) 
    OR 
    (UserId IS NOT NULL AND Guest_Email IS NULL AND Guest_Phone IS NULL)
);


ALTER TABLE Payments
ADD CONSTRAINT UNIQUE (TicketId);


-- Ensure no records with UserId IS NULL and both Guest_Email and Guest_Phone are NULL
UPDATE Tickets
SET Guest_Email = 'default@example.com', Guest_Phone = '0000000000'
WHERE UserId IS NULL AND (Guest_Email IS NULL OR Guest_Email = '') AND (Guest_Phone IS NULL OR Guest_Phone = '');

-- Ensure no records with UserId IS NOT NULL and either Guest_Email or Guest_Phone is not NULL
UPDATE Tickets
SET Guest_Email = NULL, Guest_Phone = NULL
WHERE UserId IS NOT NULL AND (Guest_Email IS NOT NULL OR Guest_Phone IS NOT NULL);
