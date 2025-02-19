import {Facebook,Instagram,Twitter,CheckCircle,Smartphone,Leaf,LineChart, Icon } from "lucide-react";

import image1 from "../assets/images/Hero.png"

export const NavLinks = [
    { href: "/", text: "Home" },
    { href: "#", text: "About Us" },
    { href: "#", text: "Contact Us" },
  ];


export const HeroImage = [
  {  image:image1  }
]




export const services = [
  {
    icon: <Smartphone/>,
    title: "Convenience",
    checklist: <CheckCircle size={16}/>,
    list:[
        "Time Saving",
        "Time Saving",
    ]  
  },
  {
    icon: <Leaf/>,
    title: "Eco-Friendliness",
    checklist: <CheckCircle size={16}/>,
    list:[
        "Time Saving",
        "Time Saving",
    ]  
  },
  {
    icon: <LineChart/>,
    title: "Efficiency",
    checklist: <CheckCircle size={16}/>,
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

export const Auth = [
  {icon:<Facebook/>,text: "Google"},
  {icon:<Facebook/>,text: "Apple"},
  {icon:<Facebook/>,text:"Facebook"}


]