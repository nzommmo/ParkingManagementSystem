import React, { useEffect, useState } from 'react';
import CTAImage from '../../assets/images/CTA.jpeg';
import Signup from '../Auth/SignUp';
import SignIn from '../Auth/SignIn';

const CTA = () => {
  const [isSignUpModalOpen, setIsSignUpModalOpen] = useState(false);
  const [isSignInModalOpen, setIsSignInModalOpen] = useState(false);

  useEffect(() => {
    // Control body scroll when modals are open
    if (isSignUpModalOpen || isSignInModalOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'auto';
    }

    // Cleanup function
    return () => {
      document.body.style.overflow = 'auto';
    };
  }, [isSignUpModalOpen, isSignInModalOpen]);

  const handleSignUpModalOpen = () => {
    setIsSignUpModalOpen(true);
    setIsSignInModalOpen(false); // Close sign in modal if open
  };

  const handleSignInModalOpen = () => {
    setIsSignInModalOpen(true);
    setIsSignUpModalOpen(false); // Close sign up modal if open
  };

  const handleSignUpModalClose = () => {
    setIsSignUpModalOpen(false);
  };

  const handleSignInModalClose = () => {
    setIsSignInModalOpen(false);
  };

  return (
    <div className="relative mt-15">
      <div className="flex flex-col md:flex-row items-stretch justify-center">
        {/* Left Section */}
        <div className="bg-Buttons py-8 pl-12 rounded-l-md flex flex-col justify-center">
          <h1 className="lg:text-3xl md:text-3xl text-2xl font-black">
            Create Your Account Today
          </h1>
          <p className="pt-1 pb-6 w-2/3 text-neutral-800">
            Enjoy Features such as Loyalty Points, Special Discounts and Ticket History.
          </p>
          <div>
            <button 
              className="bg-Light-Background px-8 py-1 rounded-md"
              onClick={handleSignUpModalOpen}  // Fixed: Changed to open the Sign Up Modal
            >
              Create Account
            </button>
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center justify-center">
          <img 
            src={CTAImage} 
            alt="Call To Action" 
            className="lg:h-[200px] w-[350px] object-cover lg:block hidden" 
          />
        </div>
      </div>

      {/* Modal Components */}
      <Signup 
        isOpen={isSignUpModalOpen} 
        onClose={handleSignUpModalClose}
        onOpenSignIn={handleSignInModalOpen}
      />
      <SignIn 
        isOpen={isSignInModalOpen} 
        onClose={handleSignInModalClose}
        onOpenSignUp={handleSignUpModalOpen}
      />
    </div>
  );
};

export default CTA;