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

-- Create Loyalty_Points table
CREATE TABLE Loyalty_Points (
    LoyaltyId INT PRIMARY KEY AUTO_INCREMENT,
    UserId INT NOT NULL,
    Points DECIMAL(10, 2) DEFAULT 0,
    Total_Points_Earned DECIMAL(10, 2) DEFAULT 0,
    Last_Earned_Date DATETIME,
    FOREIGN KEY (UserId) REFERENCES Users(UserId),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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


DELIMITER $$

CREATE TRIGGER AfterTicketInsert
AFTER INSERT ON Tickets
FOR EACH ROW
BEGIN
    -- Insert a corresponding payment record with default status 'Pending' and amount 0
    INSERT INTO Payments (
        TicketId,
        Amount,
        Payment_Method,
        Payment_Status,
        Payment_Date,
        Payment_Time
    )
    VALUES (
        NEW.TicketId, -- Ticket ID from the newly created ticket
        0, -- Set initial amount to 0
        'Cash', -- Default payment method is 'Cash'
        'Pending', -- Default payment status is 'Pending'
        NULL, -- Payment date will be set later
        NULL -- Payment time will be set later
    );
END$$

DELIMITER ;


-- First, drop the existing trigger
DROP TRIGGER IF EXISTS SetEndTimeOnPaymentInProgress;

-- Create the new BEFORE UPDATE trigger
DELIMITER $$
CREATE TRIGGER SetEndTimeOnPaymentInProgress
BEFORE UPDATE ON Tickets
FOR EACH ROW
BEGIN
    IF NEW.Status = 'Payment_In_Progress' AND OLD.Status != 'Payment_In_Progress' THEN
        SET NEW.End_Time = NOW();
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER AfterStatusUpdate
BEFORE UPDATE ON Tickets
FOR EACH ROW
BEGIN
    -- Check if the ticket's status has been updated to "Payment_In_Progress"
    IF NEW.Status = 'Payment_In_Progress' AND OLD.Status != 'Payment_In_Progress' THEN
        -- Set the End_Time directly in the NEW row
        SET NEW.End_Time = CURRENT_TIMESTAMP;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER BeforePaymentUpdate
BEFORE UPDATE ON Payments
FOR EACH ROW
BEGIN
    -- If payment status is being changed to Completed
    IF NEW.Payment_Status = 'Completed' AND OLD.Payment_Status != 'Completed' THEN
        -- Set payment date and time directly
        SET NEW.Payment_Date = CURRENT_DATE;
        SET NEW.Payment_Time = CURRENT_TIME;
        
        -- Signal that the ticket should be updated
        SET @ticket_to_update = NEW.TicketId;
        SET @update_ticket_status = TRUE;
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER AfterPaymentUpdate
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF @update_ticket_status = TRUE AND @ticket_to_update = NEW.TicketId THEN
        UPDATE Tickets SET Status = 'Paid' WHERE TicketId = NEW.TicketId;
        SET @update_ticket_status = NULL;
        SET @ticket_to_update = NULL;
    END IF;
END$$
DELIMITER ;

DELIMITER //

CREATE TRIGGER Add_Loyalty_Points_After_Payment 
AFTER UPDATE ON Payments 
FOR EACH ROW 
BEGIN 
    DECLARE user_id INT;
    DECLARE payment_amount DECIMAL(10, 2);
    DECLARE loyalty_points DECIMAL(10, 2);
    
    -- Check if payment is completed
    IF NEW.Payment_Status = 'Completed' THEN
        -- Get the associated ticket and user information
        SELECT t.UserId, p.Amount INTO user_id, payment_amount
        FROM Payments p
        JOIN Tickets t ON p.TicketId = t.TicketId
        WHERE p.PaymentId = NEW.PaymentId;
        
        -- Only add loyalty points for registered users
        IF user_id IS NOT NULL THEN
            -- Calculate loyalty points (1% of payment amount)
            SET loyalty_points = ROUND(payment_amount * 0.01, 2);
            
            -- Insert or update loyalty points
            INSERT INTO Loyalty_Points (UserId, Points, Total_Points_Earned, Last_Earned_Date)
            VALUES (user_id, loyalty_points, loyalty_points, CURRENT_TIMESTAMP)
            ON DUPLICATE KEY UPDATE 
                Points = Points + loyalty_points,
                Total_Points_Earned = Total_Points_Earned + loyalty_points,
                Last_Earned_Date = CURRENT_TIMESTAMP;
        END IF;
    END IF;
END;//

DELIMITER ;