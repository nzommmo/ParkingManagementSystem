import React, { useState, useEffect } from 'react';
import AuthImage from '../../assets/images/Auth.png';
import axiosInstance from '../../Constants/axiosInstance';
import { Auth } from '../../Constants';

const SignIn = ({ isOpen, onClose, onOpenSignUp }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  if (!isOpen) return null;

  const clearForm = () => {
    setEmail('');
    setPassword('');
  };

  const handleSignin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    setSuccess(false);

    try {
      const response = await axiosInstance.post('/login/', {
        email,
        password,
      });

      console.log('Signin Successful:', response.data);
      setSuccess(true);
      clearForm(); // Clear the form after successful submission
      setTimeout(() => {
        onClose();
      }, 2000);
    } catch (err) {
      if (err.response?.data) {
        setErrors(err.response.data);
      } else {
        setErrors({ general: err.message || 'Sign in Failed' });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleOpenSignUp = () => {
    onClose(); // Close SignIn modal first
    clearForm(); // Clear form when switching to signup
    if (onOpenSignUp) {
      onOpenSignUp(); // Then open SignUp modal
    }
  };

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div className="fixed inset-0 backdrop-blur-sm  bg-opacity-50"></div>

      {/* Modal content */}
      <div className="fixed inset-0 flex items-center justify-center">
        <div className="bg-white items-center flex md:flex-row flex-col justify-center relative z-10 max-h-[90vh] overflow-y-auto overflow-x-hidden">
          {/* Close button */}
          <button
            onClick={() => {
              clearForm();
              onClose();
            }}
            className="absolute top-2 right-2 text-gray-500 hover:text-gray-700 text-2xl"
          >
            &times;
          </button>

          <div className="flex items-center justify-center pt-16">
            <img src={AuthImage} className="lg:w-1/2 w-2/8 lg:pt-0 pt-42 mx-5" alt="" />
          </div>

          <div className="bg-white rounded shadow-md flex flex-col px-12 py-6">
            <div className="text-center">
              <h1 className="md:text-2xl text-xl">Welcome Back</h1>
              <p className="text-sm">Please enter your details to sign in</p>
              {errors.general && (
                <div className="text-red-500 text-sm mt-2">
                  {errors.general}
                </div>
              )}
              {success && (
                <div className="text-green-500 text-sm mt-2">
                  Sign in successful! Redirecting...
                </div>
              )}
            </div>

            <div className="pt-8">
              <form onSubmit={handleSignin} className="flex flex-col gap-4">
                <div className="flex flex-col gap-1">
                  <label htmlFor="Email">Email</label>
                  <input
                    type="email"
                    id="Email"
                    placeholder="johndoe@gmail.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`border ${errors.email ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {errors.email && (
                    <div className="text-red-500 text-sm">
                      {errors.email[0]}
                    </div>
                  )}
                </div>

                <div className="flex flex-col gap-1">
                  <label htmlFor="Password">Password</label>
                  <input
                    type="password"
                    id="Password"
                    placeholder="***********"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={`border ${errors.password ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {errors.password && (
                    <div className="text-red-500 text-sm">
                      {errors.password[0]}
                    </div>
                  )}
                </div>

                <div className="flex justify-between items-center text-sm">
                  <div className="flex items-center gap-2">
                    <input type="checkbox" id="remember" />
                    <label htmlFor="remember">Remember me</label>
                  </div>
                  <button type="button" className="text-blue-600 hover:text-blue-800">
                    Forgot Password?
                  </button>
                </div>

                <div className="flex justify-center mt-4">
                  <button
                    type="submit"
                    className="bg-Buttons rounded-md px-8 py-2 text-Headings w-full"
                    disabled={loading}
                  >
                    {loading ? 'Signing in...' : 'Sign in'}
                  </button>
                </div>
              </form>
            </div>

            <div className="pt-4 text-neutral-400 flex items-center justify-center gap-3">
              <hr className="w-1/4" /> <span>or Sign in with</span> <hr className="w-1/4" />
            </div>

            <div className="flex justify-center items-center mt-4 gap-3">
              {Auth.map((auth, index) => (
                <div key={index} className="flex border rounded px-4 py-1">
                  {auth.icon} {auth.text}
                </div>
              ))}
            </div>

            <div className="flex justify-center pt-4">
              <h1>
                Don't have an account?{' '}
                <button
                  type="button"
                  onClick={handleOpenSignUp}
                  className="text-Sub-headings hover:text-blue-800"
                >
                  Sign up
                </button>
              </h1>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignIn;