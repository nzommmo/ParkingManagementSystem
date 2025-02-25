import React from 'react'
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import  Home  from './Components/Homepage/Home'
import RequestGuestTicket from './Components/Tickets/RequestGuestTicket'
import RequestUserTicket from './Components/Tickets/RequestUserTicket'
import Ticket from './Components/Tickets/Ticket'

const App = () => {
  return (
      <Router>
        <Routes>
          <Route path='/' element={<Home/>}/>
          <Route path='request-guest-ticket' element={<RequestGuestTicket/>}/>
          <Route path='request-user-ticket' element={<RequestUserTicket/>}/>
          <Route path='ticket' element={<Ticket/>}/>

        
        </Routes>
      
      </Router>
  )
}

export default App