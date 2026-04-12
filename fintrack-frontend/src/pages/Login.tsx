import { login, get_user_name, type LoginRequest } from '../services/auth';
import { useState, Fragment } from 'react';
export default function Login() {
    // First we'll define the state for both email and password.
    const [formData, setFormData] = useState<LoginRequest>({ username: '', password: '' });
    const [error, setError] = useState("");
    // We need an isLogging state to avoid double submits.
    const [isLogging, setIsLogging] = useState(false);
    const [success, setSuccess] = useState(false);
    const [name, setName] = useState("");
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
            setSuccess(true);
            const fetchedName = await get_user_name();
            setName(fetchedName);

        }
        catch (err: any) {
            setError(err.response?.data?.detail || "Unknown error");
            setSuccess(false);
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
                {success && <p>Successful log-in. Welcome {name}!</p>}
            </form>
        </Fragment>
    );
}
