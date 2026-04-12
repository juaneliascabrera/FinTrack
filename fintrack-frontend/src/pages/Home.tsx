import { useAuth } from '../context/AuthContext';

export default function Home() {
    const { user, logoutSession } = useAuth();

    return (
        <div>
            <h1>Hi, {user}</h1>
            <button onClick={logoutSession}>Log Out</button>
        </div>
    );
}