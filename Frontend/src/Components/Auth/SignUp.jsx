import React, { useState } from 'react';
import AuthImage from '../../assets/images/Auth.png';
import axiosInstance from '../../Constants/axiosInstance';

const SignUp = ({ isOpen, onClose }) => {
  if (!isOpen) return null; // Hide modal when not open

  const [first_name, setFirstName] = useState('');
  const [last_name, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState({}); // Use an object to store multiple errors
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false); // State to track successful signup

  const handleSignup = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({}); // Clear previous errors
    setSuccess(false); // Reset success state

    try {
      const response = await axiosInstance.post('/signup/', {
        first_name,
        last_name,
        email,
        password,
      });

      console.log('Signup Successful:', response.data);
      setSuccess(true); // Set success state to true
      setTimeout(() => {
        onClose(); // Close modal after a short delay
      }, 2000); // Close modal after 2 seconds
    } catch (err) {
      if (err.response?.data) {
        // If the API returns field-specific errors, set them in the errors object
        setErrors(err.response.data);
      } else {
        // If no specific errors are returned, set a generic error
        setErrors({ general: err.message || 'Signup Failed' });
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='fixed inset-0 z-50'>
      {/* Full-screen backdrop blur overlay */}
      <div className='fixed inset-0 backdrop-blur-sm bg-opacity-50'></div>

      {/* Modal content */}
      <div className='fixed inset-0 flex items-center justify-center'>
        <div className='bg-white items-center flex md:flex-row flex-col justify-center relative z-10'>
          <div>
            <img src={AuthImage} className="w-1/2 mx-5" alt="" />
          </div>
          <div className='bg-white rounded shadow-md flex flex-col px-12 py-6'>
            <div className='text-center'>
              <h1 className='md:text-2xl text-xl'>Create Account</h1>
              <p className='text-sm'>Hey, Enter your details to create an account</p>
              {/* Display general errors */}
              {errors.general && (
                <div className="text-red-500 text-sm mt-2">
                  {errors.general}
                </div>
              )}
              {/* Display success message */}
              {success && (
                <div className="text-green-500 text-sm mt-2">
                  Signup successful! Redirecting...
                </div>
              )}
            </div>

            <div className='pt-8'>
              <form onSubmit={handleSignup} className='flex flex-col gap-4'>
                <div className='flex flex-col gap-1'>
                  <label htmlFor="FirstName">First Name</label>
                  <input
                    type='text'
                    placeholder='John'
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                    className={`border ${errors.first_name ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {/* Display first name errors */}
                  {errors.first_name && (
                    <div className="text-red-500 text-sm">
                      {errors.first_name[0]} {/* Display the first error message */}
                    </div>
                  )}
                </div>
                <div className='flex flex-col gap-1'>
                  <label htmlFor="LastName">Last Name</label>
                  <input
                    type="text"
                    placeholder='Doe'
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                    className={`border ${errors.last_name ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {/* Display last name errors */}
                  {errors.last_name && (
                    <div className="text-red-500 text-sm">
                      {errors.last_name[0]}
                    </div>
                  )}
                </div>
                <div className='flex flex-col gap-1'>
                  <label htmlFor="Email">Email</label>
                  <input
                    type="email"
                    placeholder='JohnDoe@gmail.com'
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className={`border ${errors.email ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {/* Display email errors */}
                  {errors.email && (
                    <div className="text-red-500 text-sm">
                      {errors.email[0]}
                    </div>
                  )}
                </div>
                <div className='flex flex-col gap-1'>
                  <label htmlFor="Password">Password</label>
                  <input
                    type="password"
                    placeholder='***********'
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className={`border ${errors.password ? 'border-red-500' : 'border-neutral-400'} px-2 py-1 rounded-md`}
                    required
                  />
                  {/* Display password errors */}
                  {errors.password && (
                    <div className="text-red-500 text-sm">
                      {errors.password[0]}
                    </div>
                  )}
                </div>
                <div>
                  <button
                    type='submit'
                    className='bg-Buttons rounded-md px-4 py-2 text-white'
                    disabled={loading}
                  >
                    {loading ? 'Signing up...' : 'Sign Up'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignUp;