import { useEffect, useState, useCallback } from 'react';
import { listAccounts } from '../services/accounts';
import { listTransactions, type Transaction } from '../services/transactions';
import { type Account } from './Accounts';
import './Home.css';

export default function Home() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [transactions, setTransactions] = useState<Transaction[]>([]);

    const fetchData = useCallback(async () => {
        try {
            const [accs, txs] = await Promise.all([
                listAccounts(),
                listTransactions(10),
            ]);
            setAccounts(accs);
            setTransactions(txs);
        } catch (error) {
            console.error("Failed to load dashboard data", error);
        }
    }, []);

    useEffect(() => {
        fetchData();

        // Listen for new transactions created from the topbar
        const handler = () => fetchData();
        window.addEventListener('transaction-created', handler);
        return () => window.removeEventListener('transaction-created', handler);
    }, [fetchData]);

    // Compute summary metrics
    const totalBalance = accounts.reduce((sum, acc) => sum + acc.balance, 0);
    const totalIncome = transactions
        .filter(tx => tx.type === 'income')
        .reduce((sum, tx) => sum + tx.amount, 0);
    const totalExpenses = transactions
        .filter(tx => tx.type === 'expense')
        .reduce((sum, tx) => sum + tx.amount, 0);

    const formatCurrency = (value: number) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
        }).format(value);
    };

    const formatDate = (timestamp: string) => {
        return new Date(timestamp).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const getTransactionIcon = (type: string) => {
        switch (type) {
            case 'income': return '↗';
            case 'expense': return '↘';
            case 'transfer': return '⇄';
            default: return '•';
        }
    };

    const getAmountPrefix = (type: string) => {
        switch (type) {
            case 'income': return '+';
            case 'expense': return '-';
            default: return '';
        }
    };

    return (
        <div className="dashboard-page">
            {/* Summary Cards */}
            <div className="summary-cards">
                <div className="summary-card balance">
                    <div className="summary-card-icon">💰</div>
                    <div className="summary-card-label">Total Balance</div>
                    <div className="summary-card-value">{formatCurrency(totalBalance)}</div>
                </div>
                <div className="summary-card income">
                    <div className="summary-card-icon">📈</div>
                    <div className="summary-card-label">Income</div>
                    <div className="summary-card-value positive">{formatCurrency(totalIncome)}</div>
                </div>
                <div className="summary-card expense">
                    <div className="summary-card-icon">📉</div>
                    <div className="summary-card-label">Expenses</div>
                    <div className="summary-card-value negative">{formatCurrency(totalExpenses)}</div>
                </div>
            </div>

            {/* Recent Transactions */}
            <div className="recent-transactions">
                <div className="recent-transactions-header">
                    <h3>Recent Transactions</h3>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        Last {transactions.length}
                    </span>
                </div>

                {transactions.length === 0 ? (
                    <div className="empty-state">
                        <div className="empty-state-icon">📭</div>
                        <p>No transactions yet. Create one to get started!</p>
                    </div>
                ) : (
                    <ul className="transaction-list">
                        {transactions.map(tx => (
                            <li key={tx.id} className="transaction-item">
                                <div className={`transaction-icon ${tx.type}`}>
                                    {getTransactionIcon(tx.type)}
                                </div>
                                <div className="transaction-details">
                                    <div className="transaction-description">
                                        {tx.description || tx.category || tx.type.charAt(0).toUpperCase() + tx.type.slice(1)}
                                    </div>
                                    <div className="transaction-meta">
                                        {tx.category && `${tx.category} · `}
                                        {formatDate(tx.timestamp)}
                                    </div>
                                </div>
                                <div className={`transaction-amount ${tx.type}`}>
                                    {getAmountPrefix(tx.type)}{formatCurrency(tx.amount)}
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}