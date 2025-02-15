import React from 'react'
import { NavLinks } from '../../Constants'

const NavBar = () => {
  return (
    <div className='relative mt-5'>
        <div className='flex justify-between items-center mx-5'>
            <div>
                <h1 className='lg:text-5xl md:text-3xl sm:text-2xl text-lg'>Park Nasi</h1>
            </div>
            <div className='flex gap-6  text-Sub-headings md:text-xl text-md'>
            {NavLinks.map((NavLink,index)=>(
                <ul key={index} >
                    <li><a href={NavLink.href}></a>{NavLink.text}</li>
                </ul>
            ))}
                
            </div>

        </div>
        
    </div>
  )
}

export default NavBar