import { login, type LoginRequest } from '../services/auth';
import { useState, Fragment } from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
    // First we'll define the state for both email and password.
    const [formData, setFormData] = useState<LoginRequest>({ username: '', password: '' });
    const [error, setError] = useState("");
    // We need an isLogging state to avoid double submits.
    const [isLogging, setIsLogging] = useState(false);
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    }

    const navigate = useNavigate();
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        setIsLogging(true);

        try {
            const data = await login(formData);
            await localStorage.setItem('token', data.access_token);
            navigate('/home');
        }
        catch (err: any) {
            setError(err.response?.data?.detail || "Unknown error");
        }
        finally {
            setIsLogging(false);
        }
    };
    return (
        <Fragment>
            <h1>Log In</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder='Email'
                    onChange={handleChange}
                    name='username'
                />
                <input
                    type="password"
                    placeholder='Password'
                    name='password'
                    onChange={handleChange} />

                <button type="submit" disabled={isLogging}>{isLogging ? "Signing in..." : "LogIn"}</button>
                {error && <p>{error}</p>}
            </form>
        </Fragment>
    );
}
