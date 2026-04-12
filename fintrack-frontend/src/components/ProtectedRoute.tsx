import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const { user, isLoading } = useAuth();
    const tokenExists = !!localStorage.getItem('token');

    if (!tokenExists) {
        return <Navigate to="/login" replace />;
    }
    if (isLoading) {
        return <div className="loading-screen">Verificando sesión...</div>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }


    return <>{children}</>;
};

export default ProtectedRoute;
