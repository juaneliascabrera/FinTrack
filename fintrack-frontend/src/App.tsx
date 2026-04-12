import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Home from './pages/Home';
import ProtectedRoute from './components/ProtectedRoute';
import PublicRoute from './components/PublicRoute';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Raíz: Redirigimos al home, y el protector decidirá si lo manda al login */}
        <Route path="/" element={<Navigate to="/home" />} />
        
        {/* Login: Solo accesible si NO estás logueado */}
        <Route 
          path="/login" 
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          } 
        />
        
        {/* Home: Solo accesible si ESTÁS logueado */}
        <Route 
          path="/home" 
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          } 
        />

        {/* Catch-all: Cualquier otra ruta manda al home */}
        <Route path="*" element={<Navigate to="/home" />} />
      </Routes>
    </Router>
  );
}

export default App;