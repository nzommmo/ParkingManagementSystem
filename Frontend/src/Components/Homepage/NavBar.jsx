import React, { useState, useEffect } from 'react';
import { NavLinks } from '../../Constants';
import SignUp from '../Auth/SignUp';
import SignIn from '../Auth/SignIn';

const NavBar = () => {
    const [isSignUpModalOpen, setIsSignUpModalOpen] = useState(false);
    const [isSignInModalOpen, setIsSignInModalOpen] = useState(false);

    const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

    // Handle body scroll when modal opens/closes
    useEffect(() => {
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

    const toggleMobileMenu = () => {
        setIsMobileMenuOpen(!isMobileMenuOpen);
    };

    const handleSignUpModalOpen = () => {
        setIsSignUpModalOpen(true);
        setIsSignInModalOpen(false); // Close sign in modal if open
        setIsMobileMenuOpen(false); // Close mobile menu when opening modal
    };

    const handleSignInModalOpen = () => {
        setIsSignInModalOpen(true);
        setIsSignUpModalOpen(false); // Close sign up modal if open
        setIsMobileMenuOpen(false); // Close mobile menu when opening modal
    };

    const handleSignUpModalClose = () => {
        setIsSignUpModalOpen(false);
    };

    const handleSignInModalClose = () => {
        setIsSignInModalOpen(false);
    };

    return (
        <div className="relative mt-5">
            <div className="flex justify-between items-center mx-5">
                <div>
                    <h1 className="lg:text-5xl md:text-3xl sm:text-2xl text-lg">Park Nasi</h1>
                </div>
                
                {/* Hamburger Menu Icon for Mobile */}
                <div className="md:hidden">
                    <button 
                        onClick={toggleMobileMenu}
                        className="p-2 hover:bg-gray-100 rounded"
                    >
                        <svg
                            className="w-6 h-6"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="M4 6h16M4 12h16m-7 6h7"
                            ></path>
                        </svg>
                    </button>
                </div>

                {/* Desktop Navigation Links */}
                <div className="hidden md:flex gap-6 items-center text-Sub-headings md:text-xl text-md">
                    {NavLinks.map((NavLink, index) => (
                        <ul key={index}>
                            <li><a href={NavLink.href}>{NavLink.text}</a></li>
                        </ul>
                    ))}
                    <button
                        className="bg-Buttons px-5 py-1 rounded-md hover:opacity-90 transition-opacity mr-3"
                        onClick={handleSignInModalOpen}
                    >
                        Login
                    </button>
                    <button
                        className="bg-white border border-Buttons px-5 py-1 rounded-md hover:opacity-90 transition-opacity"
                        onClick={handleSignUpModalOpen}
                    >
                        Sign Up
                    </button>
                </div>
            </div>

            {/* Mobile Navigation Links */}
            {isMobileMenuOpen && (
                <div className="md:hidden absolute right-0 top-full w-[200px] bg-white shadow-lg z-40">
                    <div className="flex flex-col p-4">
                        {NavLinks.map((NavLink, index) => (
                            <div key={index} className="py-2">
                                <a 
                                    href={NavLink.href} 
                                    className="block text-Sub-headings text-lg hover:bg-gray-100 px-4 py-2 rounded transition-colors"
                                >
                                    {NavLink.text}
                                </a>
                            </div>
                        ))}
                        <button
                            className="bg-Buttons px-5 py-1 rounded-md mt-2 mb-2 hover:opacity-90 transition-opacity"
                            onClick={handleSignInModalOpen}
                        >
                            Login
                        </button>
                        <button
                            className="bg-white border border-Buttons px-5 py-1 rounded-md hover:opacity-90 transition-opacity"
                            onClick={handleSignUpModalOpen}
                        >
                            Sign Up
                        </button>
                    </div>
                </div>
            )}

            {/* Modal Components */}
            <SignUp 
                isOpen={isSignUpModalOpen} 
                onClose={handleSignUpModalClose}
                onOpenSignIn={handleSignInModalOpen}  // This is for the reverse flow if needed
            />
            <SignIn 
                isOpen={isSignInModalOpen} 
                onClose={handleSignInModalClose}
                onOpenSignUp={handleSignUpModalOpen}  // Pass the function to open SignUp modal
            />
        </div>
    );
};

export default NavBar;