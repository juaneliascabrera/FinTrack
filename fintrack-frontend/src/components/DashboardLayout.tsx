import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useState } from 'react';
import CreateTransactionModal from './CreateTransactionModal';
import './DashboardLayout.css';

interface Props {
    children: React.ReactNode;
}

export default function DashboardLayout({ children }: Props) {
    const { user, logoutSession } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [showTxModal, setShowTxModal] = useState(false);

    const navItems = [
        { path: '/home', label: 'Dashboard', icon: '📊' },
        { path: '/accounts', label: 'Accounts', icon: '🏦' },
    ];

    const handleNav = (path: string) => {
        navigate(path);
        setSidebarOpen(false);
    };

    const handleLogout = () => {
        logoutSession();
        navigate('/login');
    };

    return (
        <div className="dashboard">
            {/* Mobile overlay */}
            {sidebarOpen && (
                <div
                    className="sidebar-mobile-overlay visible"
                    onClick={() => setSidebarOpen(false)}
                />
            )}

            {/* Sidebar */}
            <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
                <div className="sidebar-brand">
                    <div className="sidebar-brand-icon">💰</div>
                    <h1>FinTrack</h1>
                </div>

                <nav className="sidebar-nav">
                    {navItems.map(item => (
                        <button
                            key={item.path}
                            className={`sidebar-link ${location.pathname === item.path ? 'active' : ''}`}
                            onClick={() => handleNav(item.path)}
                        >
                            <span className="sidebar-icon">{item.icon}</span>
                            {item.label}
                        </button>
                    ))}
                </nav>

                <div className="sidebar-footer">
                    <button className="sidebar-logout" onClick={handleLogout}>
                        <span className="sidebar-icon">🚪</span>
                        Log Out
                    </button>
                </div>
            </aside>

            {/* Topbar */}
            <header className="topbar">
                <p className="topbar-greeting">
                    Welcome back, <strong>{user}</strong>
                </p>
                <div className="topbar-actions">
                    <button
                        className="btn btn-success btn-sm"
                        onClick={() => setShowTxModal(true)}
                    >
                        + Transaction
                    </button>
                </div>
            </header>

            {/* Main content */}
            <main className="dashboard-content">
                {children}
            </main>

            {/* Mobile toggle */}
            <button
                className="sidebar-toggle"
                onClick={() => setSidebarOpen(!sidebarOpen)}
            >
                {sidebarOpen ? '✕' : '☰'}
            </button>

            {/* Global Transaction Modal */}
            <CreateTransactionModal
                isOpen={showTxModal}
                onClose={() => setShowTxModal(false)}
                onSuccess={() => {
                    setShowTxModal(false);
                    // Force page re-render by reloading data
                    window.dispatchEvent(new Event('transaction-created'));
                }}
            />
        </div>
    );
}
