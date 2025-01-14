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