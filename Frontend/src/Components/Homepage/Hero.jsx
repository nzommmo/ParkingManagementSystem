import React from 'react'
import HeroImage from "../../assets/images/Hero.png"

const Hero = () => {
  return (
    <div className='mt-10'>
        <div className='flex '>
            <div className='flex flex-col mx-5 gap-3'>
                <div className='w-2/5'>
                    <h1 className='font-bold lg:text-7xl md:text-5xl text-2xl'>Revolutionizing Parking Systems</h1>
                </div>
                <div className='md:w-2/3'>
                    <p className='text-Sub-headings lg:text-2xl md:text-xl sm:text-lg text-sm'>No more paper tickets, get your E-Parking Ticket today via SMS / Email.</p>
                </div>
                <div className='flex gap-12 mt-5'>
                    <div className=''>
                        <button className='rounded-md px-4 py-2 font-medium  '>Learn More</button></div>
                    
                </div>

            </div>
            <div className='me-12'>
            <img src={HeroImage} className='md:w-full w-3/2' alt="" />
            </div>

        </div>

    </div>
  )
}

export default Hero