import { useState } from 'react';
import { createAccount } from '../services/accounts';

interface Props {
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export default function CreateAccountModal({ isOpen, onClose, onSuccess }: Props) {
    const [name, setName] = useState('');
    const [balance, setBalance] = useState(0);
    const [isSaving, setIsSaving] = useState(false);

    if (!isOpen) return null;

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        try {
            await createAccount({ name, balance });
            setName('');
            setBalance(0);
            onSuccess();
            onClose();
        } catch (error) {
            alert("Error creating account");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>New Account</h2>
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label className="form-label">Account Name</label>
                        <input
                            className="form-input"
                            placeholder="e.g. Savings, Checking..."
                            value={name}
                            onChange={e => setName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="form-group" style={{ marginTop: 'var(--space-md)' }}>
                        <label className="form-label">Initial Balance</label>
                        <input
                            className="form-input"
                            type="number"
                            placeholder="0.00"
                            value={balance}
                            onChange={e => setBalance(Number(e.target.value))}
                            step="0.01"
                        />
                    </div>
                    <div className="modal-actions">
                        <button className="btn btn-primary" type="submit" disabled={isSaving}>
                            {isSaving ? "Creating..." : "Create"}
                        </button>
                        <button className="btn btn-ghost" type="button" onClick={onClose}>
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
