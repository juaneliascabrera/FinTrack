import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { listAccounts, deleteAccount } from '../services/accounts';
import { useEffect, useState } from 'react';

export default function Accounts() {
    const [accounts, setAccounts] = useState<any[]>([])
    const navigate = useNavigate();

    const fetchAccounts = async () => {
        const data = await listAccounts();
        setAccounts(data);
    };

    useEffect(() => {
        fetchAccounts();
    }, []);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure?")) return;

        try {
            await deleteAccount(id);
            // Actualizar la lista tras borrar
            await fetchAccounts();
        } catch (error: any) {
            alert(error.response?.data?.detail || "Error. Can't delete account");
        }
    };

    return (
        <div>
            <h1>Hi there! These are your accounts:</h1>
            <ul>
                {accounts.map(acc => (
                    <li key={acc.id} style={{ marginBottom: '10px' }}>
                        {acc.name} - Balance: ${acc.balance}
                        <button
                            onClick={() => handleDelete(acc.id)}
                            style={{ marginLeft: '15px', color: 'white', backgroundColor: 'red', border: 'none', padding: '5px 10px', cursor: 'pointer', borderRadius: '4px' }}
                        >
                            Delete
                        </button>
                    </li>
                ))}
            </ul>
            <button onClick={() => navigate('../home')}>Home</button>
        </div>
    );
}