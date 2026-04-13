import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState, Fragment } from 'react'
import CreateAccountModal from '../components/CreateAccountModal';
export default function Home() {
    const { user, logoutSession } = useAuth();
    const navigate = useNavigate()
    // Pop Up State
    const [showModal, setShowModal] = useState(false);
    return (
        <Fragment>
            <div>
                <h1>Hi, {user}</h1>
                <nav>
                    <button onClick={() => setShowModal(true)}>Create Account</button>
                    <button onClick={() => navigate('/accounts')}>List Accounts</button>
                    <button onClick={logoutSession}>Log Out</button>
                </nav>
            </div>
            {<CreateAccountModal isOpen={showModal} onClose={() => setShowModal(false)} />}
        </Fragment>
    );
    // Now I want to show user-relevant endpoints such as list and create accounts.

}