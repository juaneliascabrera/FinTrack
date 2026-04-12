import { Navigate } from 'react-router-dom';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const token = localStorage.getItem('token');

    // Si no hay token, lo mandamos al login
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    // Si hay token, dejamos que vea la página
    return <>{children}</>;
};

export default ProtectedRoute;
