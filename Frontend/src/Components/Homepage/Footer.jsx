import React from 'react'
import { Company, socials, Support } from '../../Constants'

const Footer = () => {
  return (
    <div className='relative mt-15'>
        <div className=' grid lg:grid-cols-4 md:grid-cols-2 sm:grid-cols-2 md:gap-12 gap-6 mx-3'>
            <div className='flex flex-col gap-4'>
                <div>
                <h1 className='font-semibold lg:text-3xl md:text-2xl text-xl'>Park Nasi</h1>
                </div>
                <div className='w-3/4 font-bold lg:text-4xl md:text-3xl text-2xl '>
                <p>The Future of Parking Systems</p>
                </div>
            </div>
            <div>
                <div>
                <h1 className='font-semibold'>Company</h1>
                <div className='pt-4'>
                    {Company.map((company,index)=>(
                        <ul key={index} className='pb-2 text-Sub-headings'>
                            <li>{company.text}</li>
                        </ul>
                    ))}
                </div>

                </div>
            </div>
            <div>
            <div>
                <h1 className='font-semibold'>Support</h1>
                <div className='pt-4'>
                    {Support.map((support,index)=>(
                        <ul key={index} className='pb-2 text-Sub-headings'>
                            <li>{support.text}</li>
                        </ul>
                    ))}
                </div>

                </div>
            </div>
            <div className='flex flex-col gap-3'>
                <div><h1 className='lg:text-xl md:text-lg text-md'>Ready To Elevate Your Parking Experience?</h1></div>
                <div>
                    <button className='bg-Buttons px-6 py-1 rounded-md text-Headings'>
                        Get Started
                    </button>
                </div>
                
            </div>    

        </div>
        <div className='pt-3 '>
                <hr className='text-neutral-400' />
         </div>
         <div className='mx-5 my-1 flex md:flex-row flex-col gap-2 justify-between'>
            <div>
            <p className='text-Sub-headings'> &copy; {new Date().getFullYear()}  <span className='-tracking-normal'>ParkNasi All Rights Reserved</span></p>
            </div>
            <div className='flex md:flex-row flex-col md:gap-6 gap-2 text-Sub-headings'>
                <div><p>Terms & Conditions</p></div>
                <div>Privacy Policy</div>
                <div className='flex gap-2'>
                    {socials.map((social,index)=>(
                        <div key={index} className=''>
                            <p>{social.icon}</p>

                        </div>

                    ))}
                </div>

            </div>
         </div>

    </div>
  )
}

export default Footer