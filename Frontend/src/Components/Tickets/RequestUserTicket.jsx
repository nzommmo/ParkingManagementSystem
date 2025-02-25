import React, { useState, useEffect } from 'react';
import RequestImage from '../../assets/images/RequestTicket.png';
import NavBar from '../Homepage/NavBar';
import Footer from '../Homepage/Footer';
import axiosInstance from '../../Constants/axiosInstance';
import { useNavigate } from 'react-router-dom';


const RequestUserTicket = () => {
  const [phoneNumber, setPhoneNumber] = useState('');
  const [email, setEmail] = useState('');
  const [userId, setUserId] = useState('');
  const [vehicleRegistration, setVehicleRegistration] = useState('');
  // Set a default rate (as a string, if needed by the backend)
  const [rate, setRate] = useState("1");
  const [responseMessage, setResponseMessage] = useState('');

  // Retrieve the user ID from localStorage once the component mounts
  useEffect(() => {
    const storedUserId = localStorage.getItem('user_id');
    if (storedUserId) {
      setUserId(storedUserId);
    }
  }, []);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Prepare the payload as expected by the endpoint
    const payload = {
      assigned_to: vehicleRegistration,
      user: userId,
      rate: rate, // sending rate as a string "1"
    };

    try {
      const response = await axiosInstance.post('/tickets/create/', payload);
      setResponseMessage("Ticket Created Successfully");
      setPhoneNumber('');
      setEmail('');
      setVehicleRegistration('');
      setTimeout(() => {
        navigate('/ticket');
      }, 3000); // 2000ms (2 seconds) delay
      // Optionally reset rate if needed:
      // setRate("1");
    } catch (error) {
      // Handle error response and pass through the error message from the backend
      let errorMsg = "Unknown error";
      if (error.response && error.response.data && error.response.data.error) {
        errorMsg = error.response.data.error;
      } else if (error.message) {
        errorMsg = error.message;
      }
      setResponseMessage(`Failed to create ticket: ${errorMsg}`);
    }
  };

  return (
    <>
      <div>
        <NavBar />
      </div>
      <div className='relative'>
        <div className='flex flex-col justify-center items-center'>
          <div>
            <img src={RequestImage} className='w-2/3 rounded-md' alt="Request Ticket" />
          </div>
          <div>
            <h2>User Ticket Registration</h2>
          </div>
          <div className='mt-5 flex flex-col justify-center items-center'>
            <h1 className='lg:text-4xl md:text-3xl text-xl'>Enter your Vehicle Registration</h1>
            <p className='text-neutral-500 text-md text-center'>
              Provide your vehicle registration to request a ticket.
            </p>
          </div>
          <div>
            <form onSubmit={handleSubmit} className='flex flex-col gap-4 justify-center mt-5'>
              {/* Hidden inputs for user ID and rate */}
              <input type='hidden' value={userId} readOnly />
              <input type='hidden' value={rate} readOnly />
              <div>
                <input
                  type="text"
                  placeholder='Vehicle Registration'
                  className='border p-2 rounded border-black'
                  value={vehicleRegistration}
                  onChange={(e) => setVehicleRegistration(e.target.value)}
                />
              </div>
              <div className='flex justify-center items-center'>
                <button type='submit' className='bg-Buttons mt-6 rounded-md px-6 py-2'>
                  Request Ticket
                </button>
              </div>
            </form>
          </div>
          <div className='flex justify-center text-center'>
            {responseMessage && <p className='mt-4'>{responseMessage}</p>}
          </div>
        </div>
        <div>
          <Footer />
        </div>
      </div>
    </>
  );
};

export default RequestUserTicket;
