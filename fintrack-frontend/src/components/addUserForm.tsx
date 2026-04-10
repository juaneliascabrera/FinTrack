import { useState } from 'react';

const AddUserForm = ({ addUser }) => {
    const [userName, setUserName] = useState('');
    const [userEmail, setUserEmail] = useState('');
    const [userPassword, setUserPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        if (userName && userEmail && userPassword) {
            addUser(userName, userEmail, userPassword);
            setUserName('');
            setUserEmail('');
            setUserPassword('');
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
                placeholder="Name"
            />
            <input
                type="email"
                value={userEmail}
                onChange={(e) => setUserEmail(e.target.value)}
                placeholder="Email"
            />
            <input
                type="password"
                value={userPassword}
                onChange={(e) => setUserPassword(e.target.value)}
                placeholder="Password"
            />
            <button type="submit">
                Add User
            </button>
        </form>
    )
};

export default AddUserForm;

