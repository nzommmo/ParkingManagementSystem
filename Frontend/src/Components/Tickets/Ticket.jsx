import React from 'react';

const Ticket = () => {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="w-[370px]  p-4 flex flex-col items-center ">
        <h1 className="font-bold text-lg">Parking Ticket - 22-01-2025</h1>

        <div className=" gap-1 flex flex-col w-full mt-4 p-2  rounded ">
          <div className='bg-Light-Background rounded-md px-2  '>
            <div className='flex flex-col '>
                <p className='text-lg'>Galleria Mall - Langata</p>
                <p className='text-neutral-500 text-sm'>22 Jan 2025, Wednesday</p>
            </div>
          </div>
          <div className='bg-Light-Background rounded-md px-2 py-2 '>
            <div className='grid grid-cols-2 gap-6'>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Vehicle Registration</p>
                <p>KDK 239S</p>
            </div>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Ticket ID</p>
                <p>LA325478</p>
            </div>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Arrival Time</p>
                <p>04:59 Pm</p>
            </div>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>End Time</p>
                <p>06:39 pm</p>
            </div>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Duration</p>
                <p>2hrs</p>
            </div>
            <div className='flex flex-col'>
                <p className='text-sm text-neutral-500'>Total Amount</p>
                <p className='text-Headings font-bold'>Ksh 200.00</p>
            </div>

            </div>
          </div>
          <div className='bg-Light-Background rounded-md px-2 py-2 '>
            <div className='flex justify-center items-center'>
                3
            </div>
            <div className='mx-4'>
                <p><span className='text-Headings'>Note:</span></p>
            </div>

          </div>
        </div>

        <div className="mt-2 font-semibold">3</div>
      </div>
    </div>
  );
};

export default Ticket;
