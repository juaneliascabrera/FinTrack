import { useState } from 'react';
//import { createAccount } from '../services/accounts';

interface Props {
    isOpen: boolean;
    onClose: () => void;
}

export default function CreateAccountModal({ isOpen, onClose }: Props) {
    const [name, setName] = useState('');
    const [balance, setBalance] = useState('');
    const [isSaving, setIsSaving] = useState(false);

    if (!isOpen) return null; // If it's not open, it should not render anything.

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsSaving(true);
        try {
            //          await createAccount({ name, balance });
            setName('');
            setBalance('');
            onClose(); // We ended
            alert("Cuenta creada!");
        } catch (error) {
            alert("Error al crear");
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className='modal-overlay'>
            <div className='modal-content'>
                <h2>New Account</h2>
                <form onSubmit={handleSubmit}>
                    <input
                        placeholder="Account Name"
                        value={name}
                        onChange={e => setName(e.target.value)}
                        required
                    />
                    <input
                        placeholder="Balance"
                        value={balance}
                        onChange={e => setBalance(e.target.value)}
                    />
                    <button type="submit" disabled={isSaving}>Create</button>
                    <button type="button" onClick={onClose}>Close</button>
                </form>
            </div>
        </div>
    );
}
