import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

interface PublicRouteProps {
    children: React.ReactNode;
}

const PublicRoute = ({ children }: PublicRouteProps) => {
    const { user, isLoading } = useAuth();
    const token = localStorage.getItem('token');

    if (isLoading) {
        return <div className="loading-screen">Verificando sesión...</div>;
    }


    if (user || token) {
        return <Navigate to="/home" replace />;
    }


    return <>{children}</>;
};

export default PublicRoute;
