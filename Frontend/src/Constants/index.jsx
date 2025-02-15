import { Cable, icons } from "lucide-react";
import { Wrench,Shirt,Bike,Facebook,Instagram,Twitter,MapPin,Mail,Phone } from "lucide-react";

import image1 from "../assets/images/Hero.png"

export const NavLinks = [
    { href: "#", text: "Home" },
    { href: "#", text: "About Us" },
    { href: "#", text: "Contact Us" },
  ];


export const HeroImage = [
  {  image:image1  }
]




export const services = [
  {
    icon: <Cable/>,
    title: "Convenience and Efficiency",
    list:[
        "Time Saving",
        "Time Saving",
    ]  
  },
  {
    icon: <Cable/>,
    title: "Convenience and Efficiency",
    list:[
        "Time Saving",
        "Time Saving",
    ]  
  },
  {
    icon: <Cable/>,
    title: "Convenience and Efficiency",
    list:[
        "Time Saving",
        "Time Saving",
    ]  
  },
];



export const Company = [
    { href: "#", text: "About" },
    { href: "#", text: "Careers" },
    { href: "#", text: "Blog" },
  ];

export const Support = [
  { href: "#", text: "Help Center" },
  { href: "#", text: "Contact Us" },
  { href: "#", text: "API docs" },
];


export const socials = [
  {icon: <Facebook size={18}/> },
  {icon: <Instagram size={18}/>},
  {icon: <Twitter size={18}/>},

];