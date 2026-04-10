import { useState } from 'react'
import './App.css'
import AddUserForm from './components/addUserForm'
import api from './api'

function App() {
  const [message, setMessage] = useState('')

  const handleRegisterUser = async (name, email, password) => {
    try {
      const response = await api.post('/users', { name, email, password });
      setMessage(`Success! User ${response.data.name} created.`);
    } catch (error) {
      setMessage(`Error: ${error.response?.data?.detail || 'Failed to register'}`);
    }
  }

  return (
    <div className="App">
      <h1>FinTrack Management</h1>
      
      <div className="card">
        <h2>Add New User</h2>
        <AddUserForm addUser={handleRegisterUser} />
        {message && <p className="status-message">{message}</p>}
      </div>

      <p className="read-the-docs">
        Check the console for API responses.
      </p>
    </div>
  )
}

export default App
