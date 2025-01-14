CREATE VIEW TicketDetails AS
SELECT 
    t.TicketId,
    t.Assigned_TO,
    t.UserId,
    t.Guest_Email,
    t.Guest_Phone,
    t.Stay_Duration,
    t.Start_Time,
    t.End_Time,
    t.Rate_id,
    t.Status,
    t.created_at,
    IF(t.End_Time IS NULL, 0, (TIMESTAMPDIFF(MINUTE, t.Start_Time, t.End_Time) / 60.0) * pr.Rate) AS Amount
FROM 
    Tickets t
JOIN 
    Pricing_Rates pr
ON 
    t.Rate_id = pr.Rate_id;
