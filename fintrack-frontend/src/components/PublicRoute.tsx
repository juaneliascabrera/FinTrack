import { Navigate } from 'react-router-dom';

interface PublicRouteProps {
    children: React.ReactNode;
}

const PublicRoute = ({ children }: PublicRouteProps) => {
    const token = localStorage.getItem('token');

    // If there's token, we can't be in PublicRoute
    if (token) {
        return <Navigate to="/home" replace />;
    }

    // But if there's not, then we render here.
    return <>{children}</>;
};

export default PublicRoute;
