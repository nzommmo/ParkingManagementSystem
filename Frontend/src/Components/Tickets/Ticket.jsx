import React, { useEffect, useState } from "react";
import { QRCodeCanvas } from "qrcode.react";
import axiosInstance from "../../Constants/axiosInstance";

const Ticket = () => {
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);
  const [paymentStatus, setPaymentStatus] = useState(null);
  
  useEffect(() => {
    fetchLatestTicket();
  }, []);

  const fetchLatestTicket = async () => {
    try {
      const response = await axiosInstance.get("http://127.0.0.1:8000/api/tickets/");
      const tickets = response.data;
      if (tickets.length > 0) {
        const latestTicket = tickets.reduce((prev, current) => (prev.id > current.id ? prev : current));
        setTicket(latestTicket);
      }
    } catch (error) {
      console.error("Error fetching ticket:", error);
    }
  };

  const handlePayment = async () => {
    if (!ticket) return;
    
    setLoading(true);
    try {
      const response = await axiosInstance.put(`http://127.0.0.1:8000/api/tickets/${ticket.id}/update`, {
        status: "Payment_In_Progress"
      });
      
      // Update local ticket data with the updated data from response
      setTicket(response.data);
      setPaymentStatus("success");
      
      // Refresh ticket data after status update
      fetchLatestTicket();
    } catch (error) {
      console.error("Error updating ticket status:", error);
      setPaymentStatus("error");
    } finally {
      setLoading(false);
    }
  };

  // Format duration to hours and minutes
  const formatDuration = (durationMinutes) => {
    if (!durationMinutes) return "N/A";
    
    // If durationMinutes is already in format "HH:MM", return it as is
    if (typeof durationMinutes === 'string' && durationMinutes.includes(':')) {
      return durationMinutes;
    }
    
    // Convert duration to number if it's a string
    const totalMinutes = parseInt(durationMinutes, 10);
    if (isNaN(totalMinutes)) return "N/A";
    
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    
    return `${hours}h ${minutes}m`;
  };

  if (!ticket) return <p>Loading...</p>;

  const QRcode = {
    assigned_to: ticket.assigned_to,
    guest_email: ticket.guest_email,
    guest_phone: ticket.guest_phone,
    start_time: ticket.start_time,
    end_time: ticket.end_time,
    stay_duration: ticket.stay_duration,
    rate: ticket.rate,
    status: ticket.status,
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="w-[370px] p-4 flex flex-col items-center">
        <h1 className="font-bold text-lg">Parking Ticket - {new Date(ticket.start_time).toLocaleDateString()}</h1>

        <div className="gap-1 flex flex-col w-full mt-4 p-2 rounded">
          <div className='bg-Light-Background rounded-md px-2'>
            <div className='flex flex-col'>
              <p className='text-lg'>Galleria Mall - Langata</p>
              <p className='text-neutral-500 text-sm'>{new Date(ticket.start_time).toDateString()}</p>
            </div>
          </div>
          <div className='bg-Light-Background rounded-md px-2 py-2'>
            <div className='grid grid-cols-2 gap-6'>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Vehicle Registration</p>
                <p>{ticket.assigned_to}</p>
              </div>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Ticket ID</p>
                <p>{ticket.id}</p>
              </div>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Arrival Time</p>
                <p>{new Date(ticket.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
              </div>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>End Time</p>
                <p>{new Date(ticket.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
              </div>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Duration</p>
                <p>{formatDuration(ticket.duration_minutes || ticket.stay_duration)}</p>
              </div>
              <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Total Amount</p>
                <p className='text-Headings font-bold'>Ksh {ticket.amount}.00</p>
              </div>
            </div>
          </div>
          <div className='bg-Light-Background rounded-md px-2 py-2'>
            <div className='flex justify-center items-center'>
              <div className='opacity-80 py-4'>
                <QRCodeCanvas value={JSON.stringify(QRcode)} size={180} />
              </div>
            </div>
            <div className='mx-4 text-center'>
              <p><span className='text-Headings text-xs text-center'>Note: If paying by cash, kindly scan your ticket at the pay station.</span></p>
            </div>
          </div>
        </div>

        <div className="mt-4">
          {paymentStatus === "success" ? (
            <div className="text-green-600 font-medium">Proceeding to payment...</div>
          ) : ticket.status === "Payment_In_Progress" ? (
            <div className="text-blue-600 font-medium">Payment in progress</div>
          ) : ticket.status === "Paid" ? (
            <div className="text-green-600 font-medium">Ticket is already paid</div>
          ) : (
            <button 
              className={`bg-Buttons px-16 py-1 rounded-md ${loading ? 'opacity-70' : ''}`}
              onClick={handlePayment}
              disabled={loading}
            >
              {loading ? "Processing..." : "Pay"}
            </button>
          )}
          
          {paymentStatus === "error" && (
            <div className="text-red-600 text-sm mt-2">Failed to update payment status. Please try again.</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Ticket;