import { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import { get_user_name } from '../services/auth';

interface AuthContextType {
    user: string | null;
    isLoading: boolean;
    loginSession: (username: string) => void;
    logoutSession: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        // At App start we check if we already have a session.
        const initAuth = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                try {
                    const username = await get_user_name();
                    setUser(username);
                } catch (error) {
                    console.error("Token verification failed at startup", error);
                    localStorage.removeItem('token');
                    setUser(null);
                }
            }
            setIsLoading(false);
        };

        initAuth();
    }, []);

    const loginSession = (username: string) => {
        setUser(username);
    };

    const logoutSession = () => {
        localStorage.removeItem('token');
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, isLoading, loginSession, logoutSession }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return context;
};
