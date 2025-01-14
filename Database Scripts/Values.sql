-- Sample Data for Users Table
INSERT INTO Users (FirstName, LastName, Email, Password, Role) 
VALUES 
    ('John', 'Doe', 'john.doe@example.com', 'password123', 'Admin'),
    ('Jane', 'Smith', 'jane.smith@example.com', 'password123', 'User'),
    ('Bob', 'Johnson', 'bob.johnson@example.com', 'password123', 'Parking-lot Attendant');

-- Sample Data for Pricing_Rates Table
INSERT INTO Pricing_Rates (Rate, Description) 
VALUES 
    (5.00, 'Standard rate for parking'),
    (7.00, 'Premium rate for parking');

-- Sample Data for Tickets Table
INSERT INTO Tickets (Assigned_TO, UserId, Guest_Email, Guest_Phone, Start_Time, End_Time, Rate_id, Status)
VALUES 
    ('KDK 009K', 1, NULL, NULL, '2025-01-14 10:00:00', '2025-01-14 12:00:00', 1, 'Paid'),
    ('KDK 010K', 2, 'guest@example.com', '1234567890', '2025-01-14 09:30:00', NULL, 2, 'Unpaid'),
    ('KDK 012K', 3, NULL, NULL, '2025-01-14 08:00:00', '2025-01-14 10:00:00', 1, 'Payment_In_Progress');

-- Sample Data for Payments Table
-- Payment records will be inserted automatically when a ticket is created due to the trigger.
-- However, let's insert one manually to demonstrate.

INSERT INTO Payments (TicketId, Amount, Payment_Method, Payment_Status, Payment_Date, Payment_Time) 
VALUES 
    (1, 10.00, 'Cash', 'Completed', '2025-01-14', '12:05:00'),
    (2, 0, 'Bank', 'Pending', NULL, NULL),
    (3, 0, 'Mpesa', 'Pending', NULL, NULL);
