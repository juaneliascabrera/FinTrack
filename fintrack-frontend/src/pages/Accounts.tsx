import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { listAccounts } from '../services/accounts';
import { useEffect, useState } from 'react';

export default function Accounts() {
    const [accounts, setAccounts] = useState([])
    const navigate = useNavigate();
    useEffect(() => {
        const fetchAccounts = async () => {
            const data = await listAccounts();
            console.log(data);
            setAccounts(await listAccounts());
        }
        fetchAccounts();
    }, []);

    return (
        <div>
            <h1>Hi there! These are your accounts:</h1>
            <ul>
                {accounts.map(acc => (
                    <li key={acc.id}>
                        {acc.name} - Balance: ${acc.balance}
                    </li>
                ))}
            </ul>
            <button onClick={() => navigate('../home')}>Home</button>
        </div>
    );
}