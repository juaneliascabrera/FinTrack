import { Navigate } from 'react-router-dom';
import { get_user_name } from '../services/auth';
import { useState, useEffect } from 'react';

interface ProtectedRouteProps {
    children: React.ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    const [tokenExists, setTokenExists] = useState(!!localStorage.getItem('token'));

    useEffect(() => {
        const verifySession = async () => {
            if (!tokenExists) {
                return;
            }

            try {
                await get_user_name();

            } catch (error) {
                console.error("Session verification failed", error);
                setTokenExists(false);

            }
        };

        verifySession();
    }, [tokenExists]);

    if (!tokenExists) {
        return <Navigate to="/login" replace />;
    }
    return <>{children}</>;
};

export default ProtectedRoute;
