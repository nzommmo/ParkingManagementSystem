import React, { useState } from 'react'
import RequestImage from '../../assets/images/RequestTicket.png'
import NavBar from '../Homepage/NavBar'
import Footer from '../Homepage/Footer'
import axiosInstance from '../../Constants/axiosInstance'

const RequestGuestTicket = () => {

  const [phoneNumber, setPhoneNumber] = useState('')
  const [email, setEmail] = useState('')
  const [VehicleRegistration, setVehicleRegistration] = useState('')
  const [responseMessage, setResponseMessage] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Prepare the payload as expected by the endpoint
    const payload = {
      assigned_to :VehicleRegistration,
      guest_email: email,
      guest_phone: phoneNumber,
      rate:1
    }
    try {
      const response = await axiosInstance.post('/tickets/guest/',payload)
      setResponseMessage ("Ticket Created Successfully")
      setPhoneNumber('')
      setEmail('')
      setVehicleRegistration('')
    }
    catch (error) {
      // Handle Error Response
      let errorMsg = "Unknown error";
      if (error.response && error.response.data && error.response.data.error) {
        errorMsg = error.response.data.error
      } else if (error.message) {
        errorMsg =error.message;
      }
      setResponseMessage (`Failed to create ticket: ${errorMsg}`)

    }
  }


  return (
    <>
    <div>
      <NavBar/>
    </div>
    <div className='relative'>
        <div className='flex flex-col justify-center items-center '>
            <div>
                <img src={RequestImage} className='w-2/3 rounded-md' alt="" />
            </div>
            <div>
              <h2>Guest Ticket Registration</h2>
            </div>
            <div className='mt-5 flex flex-col justify-center items-center'>
                <h1 className='lg:text-4xl md:text-3xl text-xl'>Enter your Phone Number and Email</h1>
                <p className='text-neutral-500 text-md text-center'>Provide an active Phone Number and Email to receive your ticket.</p>
            </div>
            <div>
            <form onSubmit={handleSubmit} className='flex flex-col gap-4 justify-center mt-5'>
              <div>
              <input type="text"
              placeholder='Phone Number'
              className='border p-2 rounded border-black'
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
              
              />
              </div>
              <div>
                <input type="email"
                placeholder='Email'
                className='border p-2 rounded border-black'
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <input type="text"
                placeholder='Vehicle Registration'
                className='border p-2 rounded border-black'
                value={VehicleRegistration}
                onChange={(e) => setVehicleRegistration(e.target.value)}
                />
              </div>
              <div className='flex justify-center items-center '>
                <button type='submit' className='bg-Buttons mt-6 rounded-md px-6 py-2'>
                  Request Ticket
                </button>
              </div>
              </form>
             
            </div>
            <div className='flex justify-center'>
              {responseMessage && <p className='mt-4'>{responseMessage}</p>}
              </div>


        </div>
        <div>
          <Footer/>
        </div>

    </div>
    </>
  )
}

export default RequestGuestTicket