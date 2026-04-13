import api from './api';

export interface TransactionCreate {
    amount: number;
    type: 'income' | 'expense' | 'transfer';
    source_account: number;
    destination_account?: number;
    description?: string;
    category?: string;
}

export async function createTransaction(data: TransactionCreate) {
    const response = await api.post("/transactions", data);
    return response.data;
}
