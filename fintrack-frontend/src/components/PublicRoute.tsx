import { Navigate } from 'react-router-dom';

interface PublicRouteProps {
    children: React.ReactNode;
}

const PublicRoute = ({ children }: PublicRouteProps) => {
    const token = localStorage.getItem('token');

    // Si ya hay token, no lo dejamos estar en login/registro, lo mandamos al home
    if (token) {
        return <Navigate to="/home" replace />;
    }

    // Si no hay token, dejamos que vea la página pública
    return <>{children}</>;
};

export default PublicRoute;
