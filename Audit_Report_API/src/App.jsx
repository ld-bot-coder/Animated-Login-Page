import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import GoogleForm from './components/GoogleForm'
function App() {
  const [count, setCount] = useState(0)

  return (
    <>

        <GoogleForm/>
      
     
    </>
  )
}

export default App
