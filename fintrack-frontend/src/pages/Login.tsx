import { login, get_user_name, type LoginRequest } from '../services/auth';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Login.css';

export default function Login() {
    const { loginSession } = useAuth();

    const [formData, setFormData] = useState<LoginRequest>({ username: '', password: '' });
    const [error, setError] = useState("");
    const [isLogging, setIsLogging] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    }

    const navigate = useNavigate();
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLogging(true);
        setError("");

        try {
            const data = await login(formData);
            localStorage.setItem('token', data.access_token);

            // We get the name for the cloud
            const fetchedName = await get_user_name();

            // Then we upload it
            loginSession(fetchedName);

            // Navigate
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
        <div className="login-page">
            <div className="login-card">
                <div className="login-brand">
                    <div className="login-brand-icon">💰</div>
                    <h1>FinTrack</h1>
                    <p>Sign in to manage your finances</p>
                </div>

                <form className="login-form" onSubmit={handleSubmit}>
                    {error && <div className="login-error">{error}</div>}

                    <div className="form-group">
                        <label className="form-label">Email</label>
                        <input
                            className="form-input"
                            type="email"
                            placeholder="you@example.com"
                            onChange={handleChange}
                            name="username"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            className="form-input"
                            type="password"
                            placeholder="••••••••"
                            name="password"
                            onChange={handleChange}
                            required
                        />
                    </div>

                    <button
                        className="btn btn-primary login-btn"
                        type="submit"
                        disabled={isLogging}
                    >
                        {isLogging ? "Signing in..." : "Sign In"}
                    </button>
                </form>
            </div>
        </div>
    );
}
