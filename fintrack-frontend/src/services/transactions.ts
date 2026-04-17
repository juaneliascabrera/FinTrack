import api from './api';

export interface TransactionCreate {
    amount: number;
    type: 'income' | 'expense' | 'transfer';
    source_account: number;
    destination_account?: number;
    description?: string;
    category?: string;
}

export interface Transaction {
    id: number;
    amount: number;
    type: 'income' | 'expense' | 'transfer';
    description?: string;
    category?: string;
    source_account: number;
    timestamp: string;
}

export async function createTransaction(data: TransactionCreate) {
    const response = await api.post("/transactions", data);
    return response.data;
}

export async function listTransactions(limit: number = 50, offset: number = 0): Promise<Transaction[]> {
    const response = await api.get(`/transactions?limit=${limit}&offset=${offset}`);
    return response.data;
}
