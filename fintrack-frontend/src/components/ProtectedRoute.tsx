import { Navigate } from 'react-router-dom';
import { get_user_name } from '../services/auth';
interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const isValidSession = get_user_name();
    const token = localStorage.getItem('token');

    // If there's no token, we'll go to the login
    if (!token) {
        return <Navigate to="/login" replace />;
    }

    // If there's token, we'll render the page.
    return <>{children}</>;
};

export default ProtectedRoute;
