import React from 'react'
import { services } from '../../Constants'

const Info = () => {
  return (
    <div className='relative mx-5 mt-15'>
        <div className='flex flex-col items-center text-center'>
            <div>
            <h1 className='lg:text-4xl md:text-3xl sm:text-2xl text-2xl'>Parking Made Convenient</h1>
            </div>
            <div className='md:w-2/5  '>
            <p className='text-neutral-600'>Lorem ipsum dolor sit amet consectetur adipisicing elit. Incidunt rem laudantium, explicabo, tempora veniam delectus itaque </p>

            </div>

        </div>

        <div className='grid md:grid-cols-3 gap-6 mt-8 '>
                {services.map((service,index)=>(
                    <div key={index} className='rounded-md bg-Light-Background p-3'>
                        <div className='py-3z'>
                            <p>{service.icon}</p>
                            <h1 className='pt-3 text-lg font-bold'>{service.title}</h1>                        
                        </div>
                        <div className='pt-3'>
                            <ul className='flex flex-col gap-3'>
                                {service.list.map((item,index)=>(
                                    <li key={index} className='flex gap-2 items-center'>
                                    {service.checklist} {item}
                                    </li>
                                ))}
                            </ul>
                        </div>

                    </div>
                ))}

            </div>
        

    </div>
  )
}

export default Info