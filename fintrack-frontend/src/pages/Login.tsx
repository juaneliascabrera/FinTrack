import { login, type LoginRequest } from '../services/auth';
import { useState } from 'react';
import api from '../services/api'
export default function Login() {
    // First we'll define the state for both email and password.
    const [formData, setFormData] = useState<LoginRequest>({ username: '', password: '' });
    const [error, setError] = useState("");
    // We need an isLogging state to avoid double submits.
    const [isLoggin, setIsLogging] = useState(false);
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    }

    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        setIsLogging(true);
        console.log("Logging in...")
        e.preventDefault();
        try {
            const data = await login(formData);
            localStorage.setItem('token', data.access_token);
        }
        catch (err: any) {
            setError(err.response?.data?.detail || "Unknown error");
        }
        finally {
            setIsLogging(true);
        }
    };
    return (
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

            <button type="submit">Entrar</button>
        </form>
    );
}
