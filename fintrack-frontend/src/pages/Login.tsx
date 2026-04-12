import { login } from '../services/auth';

export default function Login() {
    const handleSubmit = (e: React.SubmitEvent) => {
        e.preventDefault();
        console.log("Submit");
    };
    return (
        <form onSubmit={handleSubmit}>
            <input type="email" />
            <input type="password" />
            <button type="submit">Entrar</button>
        </form>
    );
}
