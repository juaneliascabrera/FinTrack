import { useState, useEffect } from 'react';
import { createTransaction, type TransactionCreate } from '../services/transactions';
import { listAccounts } from '../services/accounts';

interface Props {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void; // To reload account list in parent
}

export default function CreateTransactionModal({ isOpen, onClose, onSuccess }: Props) {
    const [accounts, setAccounts] = useState<any[]>([]);
    
    // Form fields
    const [type, setType] = useState<'income' | 'expense' | 'transfer'>('expense');
    const [amount, setAmount] = useState<number | ''>('');
    const [sourceAccount, setSourceAccount] = useState<number | ''>('');
    const [destinationAccount, setDestinationAccount] = useState<number | ''>('');
    const [description, setDescription] = useState('');
    const [category, setCategory] = useState('');

    const [isSaving, setIsSaving] = useState(false);

    // Load accounts when modal opens
    useEffect(() => {
        if (isOpen) {
            const fetchAccounts = async () => {
                try {
                    const data = await listAccounts();
                    setAccounts(data);
                    if (data.length > 0) {
                        setSourceAccount(data[0].id); // Pre-select first account
                    }
                } catch (error) {
                    console.error("Could not load accounts", error);
                }
            };
            fetchAccounts();
        }
    }, [isOpen]);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        // Basic validations
        if (!amount || amount <= 0) {
            alert("Amount must be greater than 0");
            return;
        }
        if (!sourceAccount) {
            alert("Select a source account");
            return;
        }
        if (type === 'transfer' && !destinationAccount) {
            alert("Select a destination account for the transfer");
            return;
        }
        if (type === 'transfer' && sourceAccount === destinationAccount) {
            alert("Destination account must be different from source account");
            return;
        }

        setIsSaving(true);
        try {
            const payload: TransactionCreate = {
                type,
                amount: Number(amount),
                source_account: Number(sourceAccount),
                description: description || undefined,
                category: category || undefined,
            };

            if (type === 'transfer') {
                payload.destination_account = Number(destinationAccount);
            }

            await createTransaction(payload);
            
            // Clear form and close
            setAmount('');
            setDescription('');
            setCategory('');
            setDestinationAccount('');
            onSuccess(); // Notify parent to reload data
            onClose();
            alert("Transaction registered!");

        } catch (error: any) {
            alert(error.response?.data?.detail || "Error creating transaction.");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className='modal-overlay'>
            <div className='modal-content'>
                <h2>New Transaction</h2>
                <form onSubmit={handleSubmit}>
                    
                    <div style={{ marginBottom: '10px' }}>
                        <label>Type:</label>
                        <select value={type} onChange={e => setType(e.target.value as any)} style={{ width: '100%', padding: '5px' }}>
                            <option value="expense">Expense</option>
                            <option value="income">Income</option>
                            <option value="transfer">Transfer</option>
                        </select>
                    </div>

                    <div style={{ marginBottom: '10px' }}>
                        <label>Amount ($):</label>
                        <input
                            type='number'
                            placeholder="0.00"
                            value={amount}
                            onChange={e => setAmount(Number(e.target.value))}
                            required
                            min="0.01"
                            step="0.01"
                            style={{ width: '100%', padding: '5px' }}
                        />
                    </div>

                    <div style={{ marginBottom: '10px' }}>
                        <label>Account {type === 'transfer' ? '(Source)' : ''}:</label>
                        <select 
                            value={sourceAccount} 
                            onChange={e => setSourceAccount(Number(e.target.value))}
                            required
                            style={{ width: '100%', padding: '5px' }}
                        >
                            <option value="" disabled>Select an account</option>
                            {accounts.map(acc => (
                                <option key={acc.id} value={acc.id}>{acc.name} (${acc.balance})</option>
                            ))}
                        </select>
                    </div>

                    {type === 'transfer' && (
                        <div style={{ marginBottom: '10px' }}>
                            <label>Destination Account:</label>
                            <select 
                                value={destinationAccount} 
                                onChange={e => setDestinationAccount(Number(e.target.value))}
                                required
                                style={{ width: '100%', padding: '5px' }}
                            >
                                <option value="" disabled>Select destination account</option>
                                {accounts.map(acc => (
                                    <option key={`dest-${acc.id}`} value={acc.id}>{acc.name}</option>
                                ))}
                            </select>
                        </div>
                    )}

                    <div style={{ marginBottom: '10px' }}>
                        <label>Category (Optional):</label>
                        <input
                            type='text'
                            placeholder="e.g. Food, Salary..."
                            value={category}
                            onChange={e => setCategory(e.target.value)}
                            style={{ width: '100%', padding: '5px' }}
                        />
                    </div>

                    <div style={{ marginBottom: '15px' }}>
                        <label>Description (Optional):</label>
                        <input
                            type='text'
                            placeholder="Details..."
                            value={description}
                            onChange={e => setDescription(e.target.value)}
                            style={{ width: '100%', padding: '5px' }}
                        />
                    </div>

                    <button type="submit" disabled={isSaving} style={{ marginRight: '10px' }}>
                        {isSaving ? "Processing..." : "Register"}
                    </button>
                    <button type="button" onClick={onClose}>Cancel</button>
                </form>
            </div>
        </div>
    );
}
