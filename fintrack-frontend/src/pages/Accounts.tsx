import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { listAccounts, deleteAccount } from '../services/accounts';
import { useEffect, useState } from 'react';
import CreateTransactionModal from '../components/CreateTransactionModal';

export interface Account {
    id: number;
    name: string;
    balance: number;
    user_id: number;
}

export default function Accounts() {
    const [accounts, setAccounts] = useState<Account[]>([])
    const [showTxModal, setShowTxModal] = useState(false);
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

            await fetchAccounts();
        } catch (error: any) {
            alert(error.response?.data?.detail || "Error. Can't delete account");
        }
    };

    return (
        <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h1>Hi there! These are your accounts:</h1>
                <button onClick={() => setShowTxModal(true)} style={{ backgroundColor: '#2ecc71', color: 'white', padding: '10px', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                    + New Transaction
                </button>
            </div>
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

            <CreateTransactionModal
                isOpen={showTxModal}
                onClose={() => setShowTxModal(false)}
                onSuccess={fetchAccounts} // Recargar los saldos de las cuentas
            />
        </div>
    );
}