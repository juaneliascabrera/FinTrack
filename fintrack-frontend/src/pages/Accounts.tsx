import { listAccounts, deleteAccount } from '../services/accounts';
import { useEffect, useState, useCallback } from 'react';
import CreateAccountModal from '../components/CreateAccountModal';
import './Accounts.css';

export interface Account {
    id: number;
    name: string;
    balance: number;
    user_id: number;
}

export default function Accounts() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [showModal, setShowModal] = useState(false);

    const fetchAccounts = useCallback(async () => {
        const data = await listAccounts();
        setAccounts(data);
    }, []);

    useEffect(() => {
        fetchAccounts();

        const handler = () => fetchAccounts();
        window.addEventListener('transaction-created', handler);
        return () => window.removeEventListener('transaction-created', handler);
    }, [fetchAccounts]);

    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        }).format(value);
    };

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this account?")) return;

        try {
            await deleteAccount(id);
            await fetchAccounts();
        } catch (error: any) {
            alert(error.response?.data?.detail || "Error. Can't delete account");
        }
    };

    return (
        <div className="accounts-page">
            <div className="accounts-header">
                <h2>Your Accounts</h2>
            </div>

            <div className="accounts-grid">
                {accounts.map(acc => (
                    <div key={acc.id} className="account-card">
                        <div className="account-card-header">
                            <div className="account-card-icon">🏦</div>
                            <span className="account-card-name">{acc.name}</span>
                        </div>
                        <div>
                            <div className="account-card-balance-label">Balance</div>
                            <div className="account-card-balance">{formatCurrency(acc.balance)}</div>
                        </div>
                        <div className="account-card-actions">
                            <button
                                className="btn btn-danger btn-sm"
                                onClick={() => handleDelete(acc.id)}
                            >
                                Delete
                            </button>
                        </div>
                    </div>
                ))}

                {/* Add Account card */}
                <div className="add-account-card" onClick={() => setShowModal(true)}>
                    <span className="add-account-icon">+</span>
                    <span className="add-account-text">New Account</span>
                </div>
            </div>

            <CreateAccountModal
                isOpen={showModal}
                onClose={() => setShowModal(false)}
                onSuccess={fetchAccounts}
            />
        </div>
    );
}