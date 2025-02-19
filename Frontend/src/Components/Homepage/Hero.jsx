import React, { useState } from 'react';
import HeroImage from "../../assets/images/Hero.png";
import { Link } from 'react-router-dom';

const Hero = () => {
  const [showDrawer, setShowDrawer] = useState(false);

  return (
    <div className='mt-10'>
      <div className='flex'>
        <div className='flex flex-col mx-5 gap-3'>
          <div className='w-2/5'>
            <h1 className='font-bold lg:text-7xl md:text-5xl text-2xl'>Revolutionizing Parking Systems</h1>
          </div>
          <div className='md:w-2/3'>
            <p className='text-Sub-headings lg:text-2xl md:text-xl sm:text-lg text-sm'>
              No more paper tickets, get your E-Parking Ticket today via SMS / Email.
            </p>
          </div>
          <div className='flex md:flex-row sm:flex-row flex-col md:gap-12 gap-4 mt-5'>
            <div>
              <button className='bg-Buttons rounded-md px-4 py-2 font-medium'>
                Learn More
              </button>
            </div>
            <div>
              <button
                onClick={() => setShowDrawer(true)}
                className='bg-Buttons rounded-md px-4 py-2 font-medium'
              >
                Request Ticket
              </button>
            </div>
          </div>
        </div>
        <div className='me-12'>
          <img src={HeroImage} className='md:w-full w-3/2' alt="Hero" />
        </div>
      </div>

      {/* Overlay */}
      {showDrawer && (
        <div
          onClick={() => setShowDrawer(false)}
          className="fixed inset-0 bg-black opacity-50 z-40"
        ></div>
      )}

      {/* Side Drawer */}
      <div
        className={`fixed top-0 right-0 h-fit rounded w-64 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out ${
          showDrawer ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="p-6">
          <h2 className="text-xl font-bold mb-4">Choose Ticket Request Type</h2>
          <div className="flex flex-col gap-4">
            <Link to='/request-guest-ticket'>
              <button
                onClick={() => setShowDrawer(false)}
                className="bg-Buttons rounded-md px-4 py-2 font-medium"
              >
                Request as Guest
              </button>
            </Link>
            <Link to='/request-user-ticket'>
              <button
                onClick={() => setShowDrawer(false)}
                className="bg-Buttons rounded-md px-4 py-2 font-medium"
              >
                Request as User
              </button>
            </Link>
            <button
              onClick={() => setShowDrawer(false)}
              className="mt-4 text-red-500 hover:underline"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
